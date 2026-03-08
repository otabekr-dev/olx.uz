from .base import *  # base.py dan barcha settingslarni olamiz
from decouple import config

# -------------------------
# DEVELOPMENT SETTINGS
# -------------------------
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Debug toolbar
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # boshiga qo'shish

INTERNAL_IPS = [
    "127.0.0.1",
]

# Database (development uchun)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('db_name'),
        'USER': config('db_user'),
        'PASSWORD': config('db_pass'),
        'HOST': config('db_host', default='localhost'),
        'PORT': config('db_port', default='5432'),
    }
}

# Static files (development)
STATICFILES_DIRS = [BASE_DIR / 'static']  # devda static fayllarni topish
STATIC_ROOT = BASE_DIR / 'staticfiles'    # collectstatic ishlash uchun tayyor