from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
#router.register(r'', views.UserViewSet)

urlpatterns = [
    #path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    #allow API users to verify HMAC-signed tokens without having access to your signing key:
    #path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterAPIView.as_view(), name='register')
]
