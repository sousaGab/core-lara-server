from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    #allow API users to verify HMAC-signed tokens without having access to your signing key:
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]
