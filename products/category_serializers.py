from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'parent',
            'icon',
            'description',
            'is_active',
            'order_num',
            'created_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Bunaqa kategoriya mavjud")
        return value