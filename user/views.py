from pstats import Stats
from django.shortcuts import render
from user.models import Profile
from user.serializers import UserSerializer, DefaultUserSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView 
from rest_framework.response import Response

class DefaultViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DefaultUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet (viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

user_view = UserViewSet.as_view({'get': 'list'})


class Login(APIView):
    def post (self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please fill all fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        check_user = User.objects.filter(username=username).exists()
        
        if check_user == False:
            return Response({'error': 'Username does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # We can now create token for the user
            token, created = Token.objects.get_or_create(user=request.user) # we check if user has token use it else create it
            data = {
                'token': token.key,
                'user_id': request.user.pk,
                'username': request.user.username,
            }
            return Response({'success': 'Successfully login', 'data': data }, status = status.HTTP_200_OK)

        else :
            return Response({'error': 'Invalid login details'}, status= status.HTTP_400_BAD_REQUEST)

login_view = Login.as_view()