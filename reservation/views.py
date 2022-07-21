from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django.db.models import Q
from .models import Reservation
from .serializers import ReservationSerializer
from datetime import datetime
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrOwnerUser


def change_date_format(date):
    res = datetime.strptime(date, "%d/%m/%Y %H:%M")
    return res

class ReservationViewSet (viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user', 'experiment']
    
    def list(self, request, *args, **kwargs):
        
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self.filterDateParams(request, queryset)
        
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    
    def filterDateParams(self, request, queryset):
        
        start = '2000-01-01T00:00:00'
        end = datetime.today()

        if request.query_params.get('start_datetime'):
            start = change_date_format(request.query_params['start_datetime'])
        
        if request.query_params.get('end_datetime'):
            end = change_date_format(request.query_params['end_datetime'])
        
        queryset = queryset.filter(
            Q(start_datetime__range=[start, end]) |
            Q(end_datetime__range=[start, end])
        )
            
        return queryset
    
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        
        if 'start_datetime' in request.data:
            request.data['start_datetime'] = change_date_format(request.data['start_datetime'])

        if 'end_datetime' in request.data:
            request.data['end_datetime'] = change_date_format(request.data['end_datetime'])
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        experiment_availability = self.availability(
            experiment = request.data['experiment'], 
            start_datetime = request.data['start_datetime'], 
            end_datetime = request.data['end_datetime'],
        )

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

    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        st_date = instance.start_datetime
        end_date = instance.end_datetime
        
        if 'start_datetime' in request.data:
            request.data['start_datetime'] = change_date_format(request.data['start_datetime'])
            st_date = request.data['start_datetime']

        if 'end_datetime' in request.data:
            request.data['end_datetime'] = change_date_format(request.data['end_datetime'])
            end_date = request.data['end_datetime']
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        experiment_availability = self.availability(
            instance = instance,
            start_datetime = st_date, 
            end_datetime = end_date )
        
        if experiment_availability['available']:
            
            self.perform_update(serializer)
            
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
    
        reservations_serializer = self.get_serializer(experiment_availability['reservations'], many=True)
        response_error = {
            'message': 'unavailable datetime',
            'reservations': reservations_serializer.data,
        }
        return  Response({'error': response_error}, status=status.HTTP_400_BAD_REQUEST)
        

    def availability(self, instance=None,experiment=None, 
                     start_datetime=None, end_datetime=None):  
        available = False
        start = start_datetime
        end = end_datetime
        
        if instance : experiment = instance.experiment_id
            
        reservations = Reservation.objects.filter(Q(experiment_id=experiment)&(
            Q(start_datetime__range=[start, end]) |
            Q(end_datetime__range=[start, end])
        ))
        
        if (not reservations) or (len(reservations) == 1 and reservations[0] == instance):
            available = True
        
        return({'available': available, 'reservations': reservations})
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """    
        allow_any = ['list', 'retrieve']
        allow_auth = ['create']
        allow_owner_or_admin = ['partial_update', 'update', 'destroy']
        
        if self.action in allow_any:
            permission_classes = [permissions.AllowAny]
            
        elif self.action in allow_auth:
            permission_classes = [permissions.IsAuthenticated]
            
        elif self.action in allow_owner_or_admin:
            permission_classes = [IsAdminOrOwnerUser]
            
        return [permission() for permission in permission_classes]


@api_view(['GET'])
def get_by_user(request):
    queryset = Reservation.objects.all().filter(user=request.data['user'])
    serializer = ReservationSerializer(queryset, many=True)
    return Response(serializer.data)