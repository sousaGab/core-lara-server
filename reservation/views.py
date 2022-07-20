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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


def change_date_format(date):
    res = datetime.strptime(date, "%d/%m/%Y %H:%M")
    return res

class ReservationViewSet (viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    search_fields = ['user_id', 'experiment']
    
    def list(self, request, *args, **kwargs):
        
        queryset = self.filter_queryset(self.get_queryset())
        
        #print(queryset)
        print('prev')
        print('-'*100)

        #queryset = self.filterParams(request, queryset)
        
        print('-'*100)
        print('after')
        #print(queryset)
        
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    
    def filterParams(self, request, queryset):
        qs = queryset
        user = request.query_params.get('user') 
        
        if user:
            print(qs)
            qs.filter(Q(finished=True))
            print(qs)
        
        if request.query_params.get('experiment'):
            qs.filter(experiment_id = request.query_params.get('experiment'))
            
        #if request.query_params.get('start_datetime') and request.query_params.get('end_datetime'):
        #    queryset.filter(Q(start_datetime__range=[start, end]) |
        ##    Q(end_datetime__range=[start, end]))
        
        # st, none
        
        # none, end
            
        return qs
    
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


def filterParams(request, queryset):
    qs = queryset
    user = request.query_params.get('user') 
    
    if user:
        qs.filter(user=user)
    
    if request.query_params.get('experiment'):
        qs.filter(experiment_id = request.query_params.get('experiment'))
        
    #if request.query_params.get('start_datetime') and request.query_params.get('end_datetime'):
    #    queryset.filter(Q(start_datetime__range=[start, end]) |
    ##    Q(end_datetime__range=[start, end]))
    
    # st, none
    
    # none, end
        
    return qs

@api_view(['GET'])
def get_by_user(request):
    queryset = Reservation.objects.all().filter(user=request.data['user'])
    serializer = ReservationSerializer(queryset, many=True)
    return Response(serializer.data)