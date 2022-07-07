from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import response, status
from .serializers import RegisterSerializer
from user.models import Profile

class RegisterAPIView(GenericAPIView):
    
    serializer_class=RegisterSerializer
    
    def post(self, request):        
        
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            instance = serializer.save()
        
            #update profile
            user_profile = Profile.objects.get(user_id=instance.id)
            update_profile( 
                instance=user_profile,
                validated_data=request.data)
            
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_profile(instance, validated_data):
    fields=instance._meta.fields
    exclude=[]
    for field in fields:
        field=field.name.split('.')[-1] #to get coulmn name
        if field in exclude:
           continue
        exec("instance.%s = validated_data.get(field, instance.%s)"%(field,field))
    instance.save()
    return instance