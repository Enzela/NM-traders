from django.contrib import admin
from .models import (
    Category, Product, HeroSlide, SaleBanner,
    Stat, Testimonial, NewsletterSubscriber, SiteSetting ,
    Coupon, PaymentQR
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'old_price',
                    'is_featured', 'is_active', 'stock')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')


@admin.register(SaleBanner)
class SaleBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'order')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'is_active', 'order')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')


admin.site.register(SiteSetting)
admin.site.site_header = "NM Traders Admin"
admin.site.site_title = "NM Traders"
admin.site.index_title = "Store Management"
from .models import Coupon, PaymentQR

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'is_active')

@admin.register(PaymentQR)
class PaymentQRAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')