from .models import SiteSetting, Category


def site(request):
    cart = request.session.get('cart', {}) if hasattr(request, 'session') else {}
    return {
        'site': SiteSetting.objects.first() or SiteSetting(),
        'nav_categories': Category.objects.all()[:6],
        'cart_count': sum(cart.values()) if cart else 0,
    }