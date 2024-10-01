from rest_framework import serializers
from .models import Review
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'img_profile', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    user =  user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
