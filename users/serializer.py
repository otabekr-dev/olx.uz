from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SellerProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'avatar']


    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            return serializers.ValidationError('Bunaqa user mavjud')
        
        return value


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = [
            'id', 'shop_name', 'shop_description', 'shop_logo', 
            'region', 'district', 'address', 'rating', 'total_sales'
        ]
        read_only_fields = ['rating', 'total_sales']  

    def validate_shop_name(self, value):
        if SellerProfile.objects.filter(shop_name=value).exists():
            raise serializers.ValidationError("Bunaqa do'kon nomi mavjud.")
        return value
    
class SellerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = [
            'id',
            'user',
            'shop_name',
            'shop_description',
            'shop_logo',
            'region',
            'district',
            'address',
            'rating',
            'total_sales'
        ]
        read_only_fields = fields    

class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role']

    def validate_role(self, value):
        if value != 'SELLER':
            raise serializers.ValidationError("Foydalanuvchi faqat seller bo'lishi mumkin.")
        return value