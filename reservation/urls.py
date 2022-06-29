from rest_framework import routers
from django.urls import path, include
from .views import ReservationViewSet
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'reservation', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
