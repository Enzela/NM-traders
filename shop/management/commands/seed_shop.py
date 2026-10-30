import urllib.request
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from shop.models import Category, Product, HeroSlide, SaleBanner, Stat, Testimonial

CATEGORIES = [
    ("Living Room", "sofa"),
    ("Bedroom", "bed"),
    ("Dining Room", "utensils"),
    ("Home Office", "chair"),
    ("Storage", "archive"),
    ("Lighting", "lightbulb"),
]

PRODUCTS = [
    ("Luna Modern Accent Chair", "living-room", 480, 620, "https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=800", True),
    ("Comfort 3-Seater Sofa", "living-room", 980, 1250, "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800", True),
    ("Nordic Coffee Table", "living-room", 320, None, "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=800", False),
    ("Velvet Lounge Chair", "living-room", 540, 690, "https://images.unsplash.com/photo-1567538096621-38d2284b23ff?w=800", True),
    
    ("King Size Upholstered Bed", "bedroom", 1100, 1400, "https://images.unsplash.com/photo-1616627561950-9f746e330187?w=800", True),
    ("Queen Wooden Bed Frame", "bedroom", 850, None, "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800", False),
    ("Single Platform Bed", "bedroom", 620, 780, "https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=800", False),
    ("Bedside Nightstand", "bedroom", 180, None, "https://images.unsplash.com/photo-1532372320572-cda25653a26d?w=800", False),
    
    ("Arden Solid Wood Dining Table", "dining-room", 1290, 1580, "https://images.unsplash.com/photo-1617806118233-18e1de247200?w=800", True),
    ("6-Seater Marble Dining Set", "dining-room", 2400, None, "https://images.unsplash.com/photo-1615874959474-d609969a20ed?w=800", True),
    ("Round Dining Table", "dining-room", 780, 950, "https://images.unsplash.com/photo-1604578762246-41134e37f9cc?w=800", False),
    ("Dining Chair with Cane Back", "dining-room", 220, None, "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=800", False),
    
    ("Ergonomic Office Chair", "home-office", 480, 620, "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=800", True),
    ("Executive Leather Chair", "home-office", 890, None, "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=800", False),
    ("Visitor Chair (Set of 2)", "home-office", 380, 460, "https://images.unsplash.com/photo-1567538096621-38d2284b23ff?w=800", False),
    ("L-Shaped Office Desk", "home-office", 780, None, "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=800", True),
    ("Standing Desk", "home-office", 940, 1150, "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800", False),
    ("Bar Stool (Set of 2)", "home-office", 340, None, "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=800", True),
    
    ("Riley Storage Sideboard", "storage", 780, 950, "https://images.unsplash.com/photo-1615873968403-89e068629265?w=800", True),
    ("Oak Bookshelf 5-Tier", "storage", 420, None, "https://images.unsplash.com/photo-1594026112284-02bb6f3352fe?w=800", False),
    ("Wardrobe with Mirror", "storage", 1450, 1700, "https://images.unsplash.com/photo-1558997519-83ea9252edf8?w=800", False),
    
    ("Ceramic Table Lamp", "lighting", 120, 160, "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=800", True),
    ("Brass Floor Lamp", "lighting", 280, None, "https://images.unsplash.com/photo-1540932239986-30128078f3c5?w=800", False),
    ("Pendant Light", "lighting", 190, 240, "https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=800", True),
]

class Command(BaseCommand):
    help = "Seeds the database with products and images"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding categories...")
        for name, icon in CATEGORIES:
            Category.objects.get_or_create(name=name, defaults={"icon": icon})

        self.stdout.write("Seeding products and downloading images...")
        for (name, cat_slug, price, old_price, img_url, is_featured) in PRODUCTS:
            if Product.objects.filter(name=name).exists():
                continue
            
            cat = Category.objects.filter(name=cat_slug.replace('-', ' ').title()).first()
            if not cat:
                continue

            product = Product(
                name=name,
                category=cat,
                price=price,
                old_price=old_price,
                is_featured=is_featured,
                is_active=True,
                stock=15,
                description=f"Premium {name.lower()} crafted for ultimate comfort and style."
            )

            # Download Image
            try:
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    img_data = response.read()
                    filename = f"{name.lower().replace(' ', '_')}.jpg"
                    product.image.save(filename, ContentFile(img_data), save=False)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to download image for {name}: {e}"))

            product.save()
            self.stdout.write(f"  ✓ Added {name}")

        self.stdout.write("Seeding Hero Slides and Banners...")
        HeroSlide.objects.get_or_create(
            title="Summer Collections",
            defaults={
                "subtitle": "Up to 50% off",
                "cta_text": "Shop Now",
                "cta_link": "/products/",
                "is_active": True
            }
        )
        
        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded all demo data!"))