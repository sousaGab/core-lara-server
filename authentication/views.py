from rest_framework.generics import GenericAPIView
from rest_framework import response, status
from .serializers import RegisterSerializer, LoginSerializer
from user.models import Profile
from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class LoginAPIView(GenericAPIView):
    
    serializer_class = LoginSerializer
    
    def post(self, request):
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
                    'user_id': user.profile.id,
                    'username': user.username,
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
            }
            return response.Response (
                {'success': 'Successfully login', 'data': response_data },
                status = status.HTTP_200_OK
            )
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
       
class RegisterAPIView(GenericAPIView):
    
    serializer_class=RegisterSerializer
    
    def post(self, request):        
        
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            user_profile = Profile.objects.get(user_id=instance.id)
            update_profile( 
                profile=user_profile,
                validated_data=request.data)
            
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def update_profile(profile, validated_data):
    
    validated_data._mutable = True
    
    if 'birth_date' in validated_data:
        validated_data['birth_date'] = datetime.strptime(
            validated_data['birth_date'], "%d/%m/%Y")
    
    fields=profile._meta.fields
    exclude=[]
    for field in fields:
        field=field.name.split('.')[-1] #to get coulumn name
        if not (field in exclude):
            exec("profile.%s = validated_data.get(field, profile.%s)"%(field,field))
    profile.save()
    return profile