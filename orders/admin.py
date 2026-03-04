from django.contrib import admin

from .models import Order, Favorite, Review

admin.site.register([Order, Favorite, Review])
