# NM Traders: dynamic Django homepage

Everything on the homepage comes from the database. Edit it in the Django admin.

| What you change | Where in admin |
|---|---|
| Products, prices, discounts, badges, stock, photos | Shop → Products |
| Category circles and their order | Shop → Categories |
| Hero text and image, sale banner, newsletter text, phone/email/address | Shop → Site settings |
| Stats (customers, products sold) | Shop → Stats |
| Customer quote | Shop → Testimonials |
| Newsletter emails collected | Shop → Subscribers |

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install django pillow
django-admin startproject config .
# copy the "shop" folder from this project next to manage.py
```

### 1. config/settings.py

```python
import os   # near the top if it is not already imported

INSTALLED_APPS = [
    # ...the default apps...
    "django.contrib.humanize",
    "shop",
]

TEMPLATES = [{
    # ...keep the defaults and add one line to context_processors:
    "OPTIONS": {"context_processors": [
        # ...defaults...
        "shop.context_processors.site",
    ]},
}]

STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### 2. config/urls.py

```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3. Run

```bash
python manage.py makemigrations shop
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_shop        # optional sample products
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the shop and http://127.0.0.1:8000/admin/ to edit it.

## Notes

- Prices show as `Rs.`; change that in `home.html` if you prefer another currency.
- The cart is stored in the session and the nav shows the item count. A cart page and checkout are the next things to build.
- `seed_shop` adds placeholder stats (0) and a placeholder quote. Replace them with your real numbers and a real customer review before launch.
- For deployment, set `DEBUG = False`, serve media files with your web server or object storage, and run `collectstatic`.
