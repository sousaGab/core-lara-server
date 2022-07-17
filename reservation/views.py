import time
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django.db.models import Q
from .models import Reservation
from django.contrib.auth.models import User
from experiment.models import Experiment
from experiment.serializers import ExperimentSerializer
from .serializers import ReservationSerializer
from datetime import datetime, timedelta
from rest_framework.decorators import api_view


def change_date_format(date):
    res = datetime.strptime(date, "%d/%m/%Y %H:%M")
    return res

class ReservationViewSet (viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]
    
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        
        if request.data['start_datetime']:
            request.data['start_datetime'] = change_date_format(request.data['start_datetime'])

        if request.data['end_datetime']:
            request.data['end_datetime'] = change_date_format(request.data['end_datetime'])
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        experiment_availability = self.availability(request.data['experiment'], request.data['start_datetime'], request.data['end_datetime'])

        if experiment_availability['available']:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
     
        reservations_serializer = self.get_serializer(experiment_availability['reservations'], many=True)
        response_error = {
            'error': 'unavailable datetime',
            'reservations': reservations_serializer.data,
        }
        return  Response({'error': response_error}, status=status.HTTP_400_BAD_REQUEST)
    
    def availability(self, experiment, start_datetime, end_datetime):
        available = False
        start = start_datetime
        end = end_datetime
        
        reservations = Reservation.objects.filter(Q(experiment_id=experiment)&(
            Q(start_datetime__range=[start, end]) |
            Q(end_datetime__range=[start, end])
        ))
        
        if not reservations:
            available = True
            
        return({'available': available, 'reservations': reservations})

@api_view(['GET'])
def get_by_user(request):
    print('hehere')
    print(request.data)
    queryset = Reservation.objects.all().filter(user=request.data['user'])
    serializer = ReservationSerializer(queryset, many=True)
    return Response(serializer.data)