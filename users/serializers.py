from django.contrib.auth.hashers import make_password
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id','email','password','phone','username','first_name','last_name')

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id','email','password','phone','username','first_name','last_name')

        def update(self, instance, validated_data):
            password = validated_data.pop('password', None)
            if password:
                instance.password = make_password(password)
            return super().update(instance, validated_data)