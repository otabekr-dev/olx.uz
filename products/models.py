from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    icon = models.ImageField(
        upload_to='category/icons/',
        null=True,
        blank=True
    )
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order_num = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):

    class Condition(models.TextChoices):
        NEW = "YANGI", "Yangi"
        IDEAL = "IDEAL", "Ideal"
        GOOD = "YAXSHI", "Yaxshi"
        FAIR = "QONIQARLI", "Qoniqarli"

    class PriceType(models.TextChoices):
        FIXED = "QAT'IY", "Qat'iy"
        NEGOTIABLE = "KELISHILADI", "Kelishiladi"
        FREE = "BEPUL", "Bepul"
        EXCHANGE = "AYIRBOSHLASH", "Ayirboshlash"

    class Status(models.TextChoices):
        PENDING = "MODERATSIYADA", "Moderatsiyada"
        ACTIVE = "AKTIV", "Aktiv"
        REJECTED = "RAD_ETILGAN", "Rad etilgan"
        SOLD = "SOTILGAN", "Sotilgan"
        ARCHIVED = "ARXIVLANGAN", "Arxivlangan"

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    condition = models.CharField(max_length=20, choices=Condition.choices)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_type = models.CharField(max_length=20, choices=PriceType.choices)
    region = models.CharField(max_length=120)
    district = models.CharField(max_length=120)
    view_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f'{self.pk} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='products/images/',
        null=True,
        blank=True
    )
    order = models.PositiveIntegerField(default=0)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_id} - {self.id}'
    
    