from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Storefront
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.product_list, name='category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('newsletter/', views.newsletter_signup, name='newsletter'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Custom Dashboard
    path('management/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('management/products/', views.admin_product_list, name='admin_product_list'),
    path('management/products/add/', views.admin_product_add, name='admin_product_add'),
    path('management/coupons/', views.admin_coupon_list, name='admin_coupon_list'),
    path('management/payment-qr/', views.admin_qr_manage, name='admin_qr_manage'),
]