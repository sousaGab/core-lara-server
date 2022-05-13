from django.urls import path, include
from .views import (UserViewSet)
from rest_framework_extensions.routers import ExtendedSimpleRouter

router = ExtendedSimpleRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.url))
]