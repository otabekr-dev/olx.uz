from rest_framework import serializers

from .models import Favorite, Order
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


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'buyer',
            'seller',
            'status',
            'final_price',
            'created_at'
        ]
        read_only_fields = fields


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'buyer',
            'seller',
            'status',
            'final_price',
            'notes',
            'meeting_location',
            'meeting_time',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields

class OrderCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['product_id', 'notes']


    def validate(self, attrs):
        product_id=attrs.get('product_id')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Mahsulot mavjudmas')


        if product.status != Product.Status.ACTIVE:
            raise serializers.ValidationError('Mahsulot aktiv emas')

        attrs['product'] = product
        return attrs

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'status',
            'meeting_location',
            'meeting_time'
        ]


    def validate(self, attrs):

        instance = self.instance                
        request = self.context['request']
        user = request.user

        new_status = attrs.get('status')

        if user == instance.seller:

            if instance.status != Order.Status.PENDING:
                raise serializers.ValidationError("Seller faqat pending orderni o'zgartira oladi")

            if new_status not in [Order.Status.AGREED, Order.Status.CANCELLED]:
                raise serializers.ValidationError("Seller faqat AGREED yoki CANCELLED qilishi mumkin")

        elif user == instance.buyer:

            if instance.status != Order.Status.AGREED:
                raise serializers.ValidationError("Buyer faqat agreed orderni o'zgartira oladi")

            if new_status not in [Order.Status.COMPLETED, Order.Status.CANCELLED]:
                raise serializers.ValidationError("Buyer faqat COMPLETED yoki CANCELLED qilishi mumkin")

        else:
            raise serializers.ValidationError("Bu order sizga tegishli emas")

        return attrs