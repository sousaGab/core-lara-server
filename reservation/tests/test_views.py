from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from django.urls import reverse
from django.contrib.auth.models import User
from experiment.models import Experiment
from reservation.models import Reservation
from django.forms.models import model_to_dict
from collections import OrderedDict


'''
[ ] GET
[ ] POST
[ ] PUT
[ ] PATCH
[ ] DELETE
'''

class TestViews(APITestCase):
    
    def setUp(self):
        
        self.client = APIClient()
        self.reservation_view_url = reverse('Reservations-list')
        
        self.experiment_1 = Experiment.objects.create(
            name= 'Experiment_1', 
            type='Web',
            description= 'Some Description',
            location= 'Test Location', 
            institution= 'Fantasy Institution'
        )
        self.experiment_2 = Experiment.objects.create(
            name= 'Experiment_2', 
            type='Physical',
            description= 'Some Description',
            location= 'Test Location', 
            institution= 'Fantasy Institution'
        )
        
        self.user_1 = User.objects.create_user(
            username= 'user_1',
            password='P4ssword@321'
        )
        self.user_2 = User.objects.create_user(
            username= 'user_2',
            password='P4ssword@321'
        )
        self.admin_user = User.objects.create_superuser(
            username= 'admin_user',
            password='Admin@321'
        )
        
        self.reservation_1 = Reservation.objects.create(
            user= self.user_1,
            experiment= self.experiment_1,
            start_datetime = "2022-07-17T12:21:00",
            end_datetime = "2022-07-17T12:30:00"
        ) 
        self.reservation_2 = Reservation.objects.create(
            user= self.user_2,
            experiment= self.experiment_2,
            start_datetime = "2022-07-17T12:21:00",
            end_datetime = "2022-07-17T12:30:00"
        )
        self.reservation_3 = Reservation.objects.create(
            user= self.user_1,
            experiment= self.experiment_2,
            start_datetime = "2022-07-18T12:21:00",
            end_datetime = "2022-07-18T12:30:00"
        ) 
    
    #GET
    def test_reservation_list_GET(self):
        '''
        This will test if list request of reservation is successful
        '''
        response = self.client.get(self.reservation_view_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_GET_reservation_by_filters(self):
        '''
        This will test if list request filter of reservation is successful
        '''
        
        # Test by user
        expected_list = list(Reservation.objects.filter(user=self.user_1).values_list(named=True))
        
        params = {'user': str(self.user_1.pk)}
        response = self.client.get(self.reservation_view_url, params=params)
        #print(list(response.data['results']))
        
        response_reservation_list = []
        
        for reservation in response.data['results']:
            temp_reservation = []
            for key, value in reservation.items():
                temp = [key,value]
                temp_reservation.append(temp)
            response_reservation_list.append(temp_reservation)
        
        print('\n\n')
        print(expected_list[0][4])
        print('\n\n')
        print(list(response.data['results'][0].items()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(expected_list, response_reservation_list)
        
        
        # Test by experiment
        
        # Test by start_datetime
        
        # Test by end_datetime
    
    
    
    
    #POST
    #PUT
    #PATCH
    #DELETE    
        
    