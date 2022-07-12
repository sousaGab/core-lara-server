from pstats import Stats
from django.shortcuts import render
from user.models import Profile
from user.serializers import UserSerializer, DefaultUserSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, generics
from rest_framework import authentication 
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminOrOwnerUser

class DefaultViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DefaultUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """    
        any_methods = ['create']
        owner_methods = ['retrieve', 'partial_update', 'update', 'destroy']
        admin_methods = ['list']
        
        if self.action in any_methods:
            permission_classes = [permissions.AllowAny]
        elif self.action in owner_methods:
            permission_classes = [IsAdminOrOwnerUser]
        elif self.action in admin_methods:
            permission_classes = [permissions.IsAdminUser]
            
        return [permission() for permission in permission_classes]