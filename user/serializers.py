from .models import Profile
from django.contrib.auth.models import User
from rest_framework import serializers

class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['last_login', 'username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'name', 'email', 'is_active', 'is_staff', 'location', 'birth_date']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['location', 'birth_date']