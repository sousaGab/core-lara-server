from user.models import Profile
from user.serializers import UserSerializer, DefaultUserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminOrOwnerUser
from datetime import datetime

class DefaultViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = DefaultUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by('id')
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
     
    """
    Update User instance
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        profile = self.get_object()
        instance = profile.user
        serializer = DefaultUserSerializer(
            instance, data=request.data, partial=partial)
        
        if serializer.is_valid(raise_exception=True):
            return self.perform_update(serializer, request, *args, **kwargs)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def perform_update(self, serializer, request, *args, **kwargs):
        
        profile_serializer = self.update_profile(request, *args, **kwargs)
        
        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save()
            serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_profile(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if 'birth_date' in request.data:
            date = datetime.strptime(
                request.data['birth_date'], "%d/%m/%Y").date()
            
            request.data['birth_date'] = date
            
        serializer = UserSerializer(instance, data=request.data, partial=partial)
        
        return serializer
    
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(user, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, user, instance):
        user.delete()
        #instance.delete()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """    
        allow_any = ['create']
        allow_owner = ['retrieve', 'partial_update', 'update', 'destroy']
        allow_admin = ['list']
        
        if self.action in allow_any:
            permission_classes = [permissions.AllowAny]
        elif self.action in allow_owner:
            permission_classes = [IsAdminOrOwnerUser]
        elif self.action in allow_admin:
            permission_classes = [permissions.IsAdminUser]
            
        return [permission() for permission in permission_classes]