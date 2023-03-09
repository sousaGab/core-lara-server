from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
from experiment.models import Experiment
from reservation.models import Reservation
from django.forms.models import model_to_dict
from collections import OrderedDict
from django.core.serializers import serialize


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
            start_datetime = "2023-05-17T12:21:00",
            end_datetime = "2023-05-17T12:30:00"
        ) 
        self.reservation_2 = Reservation.objects.create(
            user= self.user_2,
            experiment= self.experiment_2,
            start_datetime = "2023-05-17T12:21:00",
            end_datetime = "2023-05-17T12:30:00"
        )
        self.reservation_3 = Reservation.objects.create(
            user= self.user_1,
            experiment= self.experiment_2,
            start_datetime = "2023-05-18T12:21:00",
            end_datetime = "2023-05-18T12:30:00"
        )
        
        self.new_data = {
            "user": str(self.user_1.pk),
            "experiment": str(self.experiment_1.pk),
            "start_datetime": "20/4/2023 12:21",
            "end_datetime": "20/4/2023 12:30"
        }
        
        self.amount_of_reservations = Reservation.objects.all().count()
    
    #GET
    def test_reservation_list_GET(self):
        '''
        This will test if list request of reservation is successful
        '''
        response = self.client.get(self.reservation_view_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    #POST
    def test_reservation_POST_without_authorization(self):
        '''
        This tests whether sending POST request in reservation without authorization is not allowed
        '''
        response = self.client.post(self.reservation_view_url, self.new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
    
    def test_reservation_POST(self):
        '''
        This tests whether sending POST request in reservation with permission is successful
        '''
        self.client.force_authenticate(user=self.user_1)
        response = self.client.post(self.reservation_view_url, self.new_data)
        reservation_created = Reservation.objects.get(id = response.data['id'])
        data_is_equal = self.compare_data(model_to_dict(reservation_created), response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations + 1)
        self.assertTrue(data_is_equal)
        self.client.force_authenticate(user=None)
    
        
    def test_reservation_POST_without_data(self):
        '''
        This tests whether sending POST request in reservation without data is not allowed
        '''
        self.client.force_authenticate(user=self.admin_user)        
        response = self.client.post(self.reservation_view_url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        self.client.force_authenticate(user=None)
        
    def test_reservation_POST_with_datetime_not_allowed(self):
        '''
        This tests whether it is not allowed to send a POST request on reservation with existing datetime
        '''
        self.client.force_authenticate(user=self.user_1)        
        
        #Test with the same data in another reservation already registered
        data = {
            "user": str(self.reservation_1.user.pk),
            "experiment": str(self.reservation_1.experiment.pk),
            "start_datetime": self.change_br_format(self.reservation_1.start_datetime),
            "end_datetime": self.change_br_format(self.reservation_1.end_datetime)
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        #Test with the date within the range of another reservation already registered
        data = {
            "user": str(self.reservation_1.user.pk),
            "experiment": str(self.reservation_1.experiment.pk),
            "start_datetime": "17/05/2023 12:22",
            "end_datetime": "17/05/2023 12:29"
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        #Test with the start_datetime within the range of another reservation already registered
        data = {
            "user": str(self.reservation_1.user.pk),
            "experiment": str(self.reservation_1.experiment.pk),
            "start_datetime": "17/05/2023 12:22",
            "end_datetime": "17/05/2023 13:00"
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        
        #Test with the end_datetime within the range of another reservation already registered
        data = {
            "user": str(self.reservation_1.user.pk),
            "experiment": str(self.reservation_1.experiment.pk),
            "start_datetime": "17/05/2023 12:00",
            "end_datetime": "17/05/2023 12:25"
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        self.client.force_authenticate(user=None)
        
    #PUT
    def test_reservation_PUT_without_authorization(self):
        '''
        This tests whether sending PUT request in reservation without authorization is not allowed
        '''
        response = self.client.put(self.reservation_view_url, self.new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
    '''
    def test_reservation_POST(self):
        
        This tests whether sending POST request in reservation with permission is successful
       
        self.client.force_authenticate(user=self.user_1)
        response = self.client.post(self.reservation_view_url, self.new_data)
        reservation_created = Reservation.objects.get(id = response.data['id'])
        data_is_equal = self.compare_data(model_to_dict(reservation_created), response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations + 1)
        self.assertTrue(data_is_equal)
        self.client.force_authenticate(user=None)
    '''
    '''   
    def test_reservation_POST_without_data(self):
       
        This tests whether sending POST request in reservation without data is not allowed
       
        self.client.force_authenticate(user=self.admin_user)        
        response = self.client.post(self.reservation_view_url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        self.client.force_authenticate(user=None)
    '''   
    '''
    def test_reservation_POST_with_datetime_not_allowed(self):
       
        This tests whether it is not allowed to send a POST request on reservation with existing datetime
       
        self.client.force_authenticate(user=self.user_1)        
        
        #Test with the same data in another reservation already registered
        data = {
            "user": str(self.reservation_1.user.pk),
            "experiment": str(self.reservation_1.experiment.pk),
            "start_datetime": self.change_br_format(self.reservation_1.start_datetime),
            "end_datetime": self.change_br_format(self.reservation_1.end_datetime)
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        #Test with the date within the range of another reservation already registered
        data = {
            "user": str(self.reservation_1.user.pk),
            "experiment": str(self.reservation_1.experiment.pk),
            "start_datetime": "17/05/2023 12:22",
            "end_datetime": "17/05/2023 12:29"
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        #Test with the start_datetime within the range of another reservation already registered
        data = {
            "user": str(self.reservation_1.user.pk),
            "experiment": str(self.reservation_1.experiment.pk),
            "start_datetime": "17/05/2023 12:22",
            "end_datetime": "17/05/2023 13:00"
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        
        #Test with the end_datetime within the range of another reservation already registered
        data = {
            "user": str(self.reservation_1.user.pk),
            "experiment": str(self.reservation_1.experiment.pk),
            "start_datetime": "17/05/2023 12:00",
            "end_datetime": "17/05/2023 12:25"
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        self.client.force_authenticate(user=None)
    '''
    #PATCH
    #DELETE    
    
    
    
    
    def compare_data(self, data_1, data_2):
        
        keys = ['id', 'user', 'experiment', 'start_datetime', 'end_datetime', 'showed_up', 'finished', 'description']    
        for key in keys:
            
            if key == 'start_datetime' or key == 'end_datetime':
                datetime_1 = str(data_1[key]) 
                datetime_2 = str(self.change_date_format(data_2[key])) 
                if datetime_1  != datetime_2 : return False
            else :
                if data_1[key] != data_2[key] : return False
                
        return True
    
    def change_date_format(self, date):
        res = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        return res
    
    def change_br_format(self, date):
        res = self.change_date_format(date).strftime("%d/%m/%Y %H:%M")
        return res