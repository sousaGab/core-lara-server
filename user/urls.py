from rest_framework import routers
from django.urls import path, include
from .views import Login, UserViewSet
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', Login.as_view(), name='login'),
]
