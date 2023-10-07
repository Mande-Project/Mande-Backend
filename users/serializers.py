from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id','email','password','phone','username','first_name','last_name')

class CustomUserSerializer(UserSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id','email','password','phone','username','first_name','last_name')