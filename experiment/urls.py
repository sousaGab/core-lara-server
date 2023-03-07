from rest_framework import routers
from django.urls import path, include
from .views import ExperimentViewSet
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'', ExperimentViewSet, basename='Experiments')

urlpatterns = [
    path('', include(router.urls)),
]
