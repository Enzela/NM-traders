from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=60, blank=True, help_text="Emoji or Font Awesome class")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    badge = models.CharField(max_length=30, blank=True, help_text="e.g. New, Sale, Hot")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int(100 - (self.price / self.old_price * 100))
        return 0

    def __str__(self):
        return self.name


class HeroSlide(models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=200, blank=True)
    cta_text = models.CharField(max_length=40, default="Shop Now")
    cta_link = models.CharField(max_length=200, default="/products/")
    image = models.ImageField(upload_to='hero/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class SaleBanner(models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=200, blank=True)
    cta_text = models.CharField(max_length=40, default="Shop the Sale")
    cta_link = models.CharField(max_length=200, default="/products/")
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Stat(models.Model):
    label = models.CharField(max_length=60)
    value = models.CharField(max_length=30, help_text="e.g. 10K+, 25+, 5★")
    icon = models.CharField(max_length=60, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value} {self.label}"


class Testimonial(models.Model):
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=80, blank=True)
    quote = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=80, default="NM Traders")
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    topbar_text = models.CharField(max_length=200, default="Free delivery on orders over Rs. 5,000")
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'Site Setting'


# --- NEW MODELS FOR COUPONS AND PAYMENT QR ---

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="e.g. DIWALI50")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in Rs.")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code


class PaymentQR(models.Model):
    qr_image = models.ImageField(upload_to='payment_qr/', help_text="Upload your eSewa/Khalti QR code here")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Payment QR Code"