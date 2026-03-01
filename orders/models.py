from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user_id} - {self.product_id}'


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "KUTILYAPTI", "Kutilyapti"
        AGREED = "KELISHILGAN", "Kelishilgan"
        PURCHASED = "SOTIB_OLINGAN", "Sotib olingan"
        CANCELLED = "BEKOR_QILINGAN", "Bekor qilingan"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_made'
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_received'
    )
    final_price = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    meeting_location = models.CharField(max_length=255, blank=True)
    meeting_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.product_id}'


class Review(models.Model):
    order = models.OneToOneField(
        'Order',
        on_delete=models.CASCADE,
        related_name='review'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_written'
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.rating}'
