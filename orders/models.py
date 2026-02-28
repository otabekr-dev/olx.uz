from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'KUTILYAPTI', 'Kutilyapti'
        AGREED = 'KELISHILGAN', 'Kelishilgan'
        BOUGHT = 'SOTIB_OLINGAN', 'Sotib Olingan'
        CANCELLED = 'BEKOR_QILINGAN', 'Bekor Qilingan'
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    final_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=Status.choices
    )
    meeting_location = models.CharField(max_length=200, blank=True, null=True)
    meeting_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    pass    