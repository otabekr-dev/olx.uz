from rest_framework import serializers
from .models import Product, ProductImage, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'price_type', 'region', 'district',
            'view_count', 'created_at'
        ]
        read_only_fields = fields


class ProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True, read_only=True)
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'category', 'title', 'description', 'condition',
            'price', 'price_type', 'region', 'district', 'view_count',
            'favorite_count', 'status', 'created_at', 'updated_at',
            'published_at', 'expires_at', 'images'
        ]
        read_only_fields = [
            'id', 'seller', 'view_count', 'favorite_count', 'status',
            'created_at', 'updated_at', 'published_at', 'expires_at', 'images'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'category', 'title', 'description', 'condition',
            'price', 'price_type', 'region', 'district'
        ]

    def validate(self, attrs):
        price = attrs.get('price')
        price_type = attrs.get('price_type')

        if price is not None and price < 0:
            raise serializers.ValidationError("Narx manfiy bo'lishi mumkin emas")
        if price_type == Product.PriceType.FREE and price != 0:
            raise serializers.ValidationError("Bepul mahsulotda narx bo'lmaydi")
        if price_type != Product.PriceType.FREE and price == 0:
            raise serializers.ValidationError("Mahsulot bepul bo'lmasa narx kiritish shart")
        return attrs


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'category', 'title', 'description', 'condition',
            'price', 'price_type', 'region', 'district'
        ]

    def validate(self, attrs):
        instance = self.instance
        price = attrs.get('price', instance.price)
        price_type = attrs.get('price_type', instance.price_type)

        if price < 0:
            raise serializers.ValidationError("Narx manfiy bo'lmaydi")
        if price_type == Product.PriceType.FREE and price != 0:
            raise serializers.ValidationError("Bepul mahsulot narxi bo'lmaydi")
        if price_type != Product.PriceType.FREE and price == 0:
            raise serializers.ValidationError("Mahsulot bepul bo'lmasa narx kiriting")
        return attrs