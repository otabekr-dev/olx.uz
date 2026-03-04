from django.contrib import admin

from .models import Product, ProductImage, Category

admin.site.register([Product, ProductImage, Category])