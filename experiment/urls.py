from rest_framework import routers
from django.urls import path, include
from .views import ExperimentViewSet
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'experiments', ExperimentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
