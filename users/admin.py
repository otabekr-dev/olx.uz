from django.contrib import admin

from .models import SellerProfile, CustomUser

admin.site.register([SellerProfile, CustomUser])