from django.shortcuts import render
from pandas import Series
from rest_framework.generics import GenericAPIView
from rest_framework import response, status
from .serializers import RegisterSerializer, LoginSerializer
from user.models import Profile
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class LoginAPIView(GenericAPIView):
    
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            
            if serializer.is_valid():
                username = serializer.data['username']
                password = serializer.data['password']
                user = authenticate(username = username, password = password)
                
                if user is None:
                    return response.Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
                    
                refresh = RefreshToken.for_user(user)
                
                response_data = {
                        'user_id': user.id,
                        'username': user.username,
                        'refresh_token': str(refresh),
                        'access_token': str(refresh.access_token),
                }
                return response.Response (
                    {'success': 'Successfully login', 'data': response_data },
                    status = status.HTTP_200_OK
                )
                
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e :
            print(e)

"""
class Instance:
    def __init__(self,id):
        self.id = id
"""        
class RegisterAPIView(GenericAPIView):
    
    serializer_class=RegisterSerializer
    
    def post(self, request):        
        
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            #instance = Instance(6)
            #update profile
            user_profile = Profile.objects.get(user_id=instance.id)
            update_profile( 
                profile=user_profile,
                validated_data=request.data)
            
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_profile(profile, validated_data):
    
    if 'birth_date' in validated_data:
        validated_data['birth_date'] = datetime.strptime(
            validated_data['birth_date'], "%d/%m/%Y")
    
    fields=profile._meta.fields
    exclude=[]
    for field in fields:
        field=field.name.split('.')[-1] #to get coulumn name
        if field in exclude:
           continue
        exec("profile.%s = validated_data.get(field, profile.%s)"%(field,field))
    profile.save()
    return profile

"""   
class LoginAPIView(GenericAPIView):
    
    def post (self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return response.Response({'error': 'Please fill all fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        check_user = User.objects.filter(username=username).exists()
        
        if check_user == False:
            return response.Response({'error': 'Username does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            pass
            
         
        login(request, user)
            # We can now create token for the user
            token, created = Token.objects.get_or_create(user=request.user) # we check if user has token use it else create it
            data = {
                'token': token.key,
                'user_id': request.user.pk,
                'username': request.user.username,
            }
            return response.Response({'success': 'Successfully login', 'data': data }, status = status.HTTP_200_OK)

        else :
            return response.Response({'error': 'Invalid login details'}, status= status.HTTP_400_BAD_REQUEST)

login_view = Login.as_view()
        
        """ 
        