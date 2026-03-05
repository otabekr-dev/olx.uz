from rest_framework import serializers
from .models import Favorite

from products.models import Product

class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = [
            'id',
            'product',
            'created_at',
        ]
        read_only_fields = fields
        
class FavoriteCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = [
            'product_id'
        ]

    def validated_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError('Product mavjud emas')
        return value            