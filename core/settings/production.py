from .base import *  # base.py dan barcha settingslarni olamiz
from decouple import config, Csv

# -------------------------
# PRODUCTION SETTINGS
# -------------------------
DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())  # .env orqali belgilash

# Database (production uchun)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('db_name'),
        'USER': config('db_user'),
        'PASSWORD': config('db_pass'),
        'HOST': config('db_host'),
        'PORT': config('db_port', default='5432'),
    }
}

# Static files (production)
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic shundan oladi
STATICFILES_DIRS = []  # productionda STATICFILES_DIRS kerak emas