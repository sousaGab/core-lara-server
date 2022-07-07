import this
from .models import Profile
from django.contrib.auth.models import User
from rest_framework import serializers

class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['last_login', 'username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined']

class UserSerializer(serializers.ModelSerializer):

    personal = serializers.SerializerMethodField()
    def get_personal(self, obj):
        p = User.objects.all().filter(id = obj.user_id)
        serializer = DefaultUserSerializer(instance=p, many=True)
        return serializer.data
    
    class Meta:
        model = Profile
        fields = ['id', 'location', 'personal']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['location', 'birth_date']