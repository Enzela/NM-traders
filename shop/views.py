from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required   
from django.db.models import Q
import random

from .models import (
    Product, Category, HeroSlide, SaleBanner,
    Stat, Testimonial, NewsletterSubscriber, Coupon, PaymentQR
)

# ==========================================
# STOREFRONT VIEWS
# ==========================================

def home(request):
    context = {
        'hero_slides':  HeroSlide.objects.filter(is_active=True),
        'categories':   Category.objects.all(),
        'featured':     Product.objects.filter(is_featured=True, is_active=True)[:8],
        'sale_banner':  SaleBanner.objects.filter(is_active=True).first(),
        'stats':        Stat.objects.all(),
        'testimonials': Testimonial.objects.filter(is_active=True),
    }
    return render(request, "shop/home.html", context)


def product_list(request, slug=None):
    products = Product.objects.filter(is_active=True)
    category = None
    
    if slug:
        category = Category.objects.filter(slug=slug).first()
        if not category:
            return redirect('shop:product_list')
        products = products.filter(category=category)
        
    query = request.GET.get('q', '').strip()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
    return render(request, 'shop/product_list.html', {
        'products': products,
        'category': category,
        'categories': Category.objects.all(),
        'search_query': query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]
    return render(request, "shop/product_detail.html", {
        'product': product,
        'related': related,
    })


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'count': sum(cart.values())})

    messages.success(request, f'{product.name} added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'shop:home'))


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(pk=int(pid), is_active=True)
            subtotal = p.price * qty
            total += subtotal
            items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            continue
    return render(request, "shop/cart.html", {'items': items, 'total': total})


def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(pk=int(pid), is_active=True)
            subtotal = p.price * qty
            total += subtotal
            items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            continue
            
    payment_qr = PaymentQR.objects.filter(is_active=True).first()
    order_id = f"NM-{random.randint(10000, 99999)}"

    return render(request, 'shop/checkout.html', {
        'items': items, 
        'total': total,
        'payment_qr': payment_qr,
        'order_id': order_id
    })


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, 'Thanks for subscribing!')
    return redirect('shop:home')


# ==========================================
# AUTHENTICATION VIEWS (Login, Register, Logout)
# ==========================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('shop:home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('shop:login')
            
    return render(request, 'shop/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('shop:register')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('shop:register')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('shop:home')
        
    return render(request, 'shop/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('shop:home')


# ==========================================
# CUSTOM DASHBOARD VIEWS
# ==========================================

@staff_member_required
def admin_dashboard(request):
    recent_products = Product.objects.all().order_by('-created_at')[:3]
    return render(request, 'admin_panel/dashboard.html', {'recent_products': recent_products})


@staff_member_required
def admin_product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/product_list.html', {'products': products})


@staff_member_required
def admin_product_add(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            product = Product.objects.create(
                name=name,
                category_id=request.POST.get('category'),
                price=request.POST.get('price'),
                old_price=request.POST.get('old_price') or None,
                description=request.POST.get('description', ''),
                stock=request.POST.get('stock', 0),
                is_featured=request.POST.get('is_featured') == 'on',
                is_active=request.POST.get('is_active') == 'on'
            )
            
            if 'image' in request.FILES:
                product.image = request.FILES['image']
                product.save()
                
            messages.success(request, f'Product "{name}" created successfully!')
            return redirect('shop:admin_product_list')
            
        except Exception as e:
            messages.error(request, f'Error creating product: {e}')
            
    return render(request, 'admin_panel/product_form.html', {'categories': categories})


@staff_member_required
def admin_coupon_list(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        discount = request.POST.get('discount_amount')
        if code and discount:
            Coupon.objects.create(code=code, discount_amount=discount)
            messages.success(request, f'Coupon "{code}" created!')
            return redirect('shop:admin_coupon_list')
            
    coupons = Coupon.objects.all().order_by('-id')
    return render(request, 'admin_panel/coupon_list.html', {'coupons': coupons})


@staff_member_required
def admin_qr_manage(request):
    qr = PaymentQR.objects.filter(is_active=True).first()
    
    if request.method == 'POST':
        if 'qr_image' in request.FILES:
            PaymentQR.objects.all().update(is_active=False)
            new_qr = PaymentQR(qr_image=request.FILES['qr_image'], is_active=True)
            new_qr.save()
            messages.success(request, 'Payment QR updated successfully!')
            return redirect('shop:admin_qr_manage')
            
    return render(request, 'admin_panel/qr_manage.html', {'qr': qr})