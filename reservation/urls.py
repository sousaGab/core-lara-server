from rest_framework import routers
from django.urls import path, include
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'', views.ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get_reservation_by_user/', views.get_by_user)
]
