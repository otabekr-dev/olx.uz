from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        SELLER = "SELLER", "Seller"

    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    avatar = models.ImageField(
        upload_to="users/avatars/",   
        blank=True,
        null=True,
        default="users/avatars/default.jpg" 
    )

    def __str__(self):
        return f'{self.id} {self.username}' 
    

    @property
    def is_seller(self):
        return self.role == self.Role.SELLER

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER

class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=120, unique=True)
    shop_description = models.TextField(null=True, blank=True)
    shop_logo = models.ImageField(
        upload_to="shops/logos/",
        blank=True,
        null=True,
        default="shops/logos/default_shop.jpg"
    )
    region = models.CharField(max_length=120)
    district = models.CharField(max_length=120,null=True, blank=True)
    address = models.CharField(max_length=120,null=True, blank=True)
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_sales = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.shop_name}'
    