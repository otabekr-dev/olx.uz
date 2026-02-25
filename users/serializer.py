from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True)
    confirm = serializers.CharField(write_only=True, required=True)
    avatar = serializers.ImageField(required=False)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm']:
            return serializers.ValidationError('Parollar mos emas')
        
        return attrs
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            return serializers.ValidationError('Bunaqa user mavjud')
        
        return value