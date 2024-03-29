from rest_framework import serializers
from django.contrib.auth.models import User


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=128, min_length=6)
    
    class Meta:
        model = User
        fields = ('username', 'password')
    

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)