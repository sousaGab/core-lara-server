from rest_framework import viewsets
from rest_framework import permissions
from .models import Reservation
from .serializers import ReservationSerializer

class ReservationViewSet (viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serialize_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]