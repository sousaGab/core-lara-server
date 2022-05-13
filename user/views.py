from django.shortcuts import render
from user.models import Profile
from rest_framework import viewsets
from rest_framework import permissions
from user.serializers import UserSerializer, DefaultUserSerializer
from django.contrib.auth.models import User

class UserViewSet (viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class DefaultViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DefaultUserSerializer
    permission_classes = [permissions.IsAuthenticated]