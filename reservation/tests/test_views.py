from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
from experiment.models import Experiment
from reservation.models import Reservation
from django.forms.models import model_to_dict


class TestViews(APITestCase):
    
    def setUp(self):
        
        self.client = APIClient()
        self.reservation_view_url = reverse('Reservations-list')
        
        self.experiment_1 = Experiment.objects.create(
            name= 'Experiment_1', 
            type='Web',
            description= 'Some Description',
            location= 'Test Location', 
            institution= 'Fantasy Institution',
            schedule_time = 60
        )
        self.experiment_2 = Experiment.objects.create(
            name= 'Experiment_2', 
            type='Physical',
            description= 'Some Description',
            location= 'Test Location', 
            institution= 'Fantasy Institution',
            schedule_time = 120
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
            start_datetime = '2023-05-17T12:21:00',
            end_datetime = '2023-05-17T12:30:00'
        ) 
        self.reservation_2 = Reservation.objects.create(
            user= self.user_2,
            experiment= self.experiment_2,
            start_datetime = '2023-05-17T12:21:00',
            end_datetime = '2023-05-17T12:30:00'
        )
        self.reservation_3 = Reservation.objects.create(
            user= self.user_1,
            experiment= self.experiment_2,
            start_datetime = '2023-05-17T12:00:00',
            end_datetime = '2023-05-17T12:10:00'
        )
        
        self.new_data = {
            'user': str(self.user_1.pk),
            'experiment': str(self.experiment_1.pk),
            'start_datetime': '20/4/2023 12:21',
            'end_datetime': '20/4/2023 12:30'
        }
        
        self.update_data = {
            'user': str(self.reservation_1.user.pk),
            'experiment': str(self.reservation_1.experiment.pk),
            'start_datetime': '17/05/2023 12:00',
            'end_datetime': '17/05/2023 12:40'
        }
        
        self.patch_data = {
           'start_datetime': '17/05/2023 12:15', 
        }
        
        self.amount_of_reservations = Reservation.objects.all().count()
    
    #GET
    def test_reservation_list_GET(self):
        '''
        This will test if list request of reservation is successful
        '''
        response = self.client.get(self.reservation_view_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_reservation_GET_element(self):
        '''
        This will test if GET request of reservation is successful
        '''
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'
        response = self.client.get(url)
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
            'user': str(self.reservation_1.user.pk),
            'experiment': str(self.reservation_1.experiment.pk),
            'start_datetime': self.change_br_format(self.reservation_1.start_datetime),
            'end_datetime': self.change_br_format(self.reservation_1.end_datetime)
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        #Test with the date within the range of another reservation already registered
        data = {
            'user': str(self.reservation_1.user.pk),
            'experiment': str(self.reservation_1.experiment.pk),
            'start_datetime': '17/05/2023 12:22',
            'end_datetime': '17/05/2023 12:29'
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        #Test with the start_datetime within the range of another reservation already registered
        data = {
            'user': str(self.reservation_1.user.pk),
            'experiment': str(self.reservation_1.experiment.pk),
            'start_datetime': '17/05/2023 12:22',
            'end_datetime': '17/05/2023 13:00'
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        
        
        #Test with the end_datetime within the range of another reservation already registered
        data = {
            'user': str(self.reservation_1.user.pk),
            'experiment': str(self.reservation_1.experiment.pk),
            'start_datetime': '17/05/2023 12:00',
            'end_datetime': '17/05/2023 12:25'
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
                
        #Test with the start_datetime before and end_datetime after the range of another reservation already registered
        data = {
            'user': str(self.reservation_1.user.pk),
            'experiment': str(self.reservation_1.experiment.pk),
            'start_datetime': '17/05/2023 12:00',
            'end_datetime': '17/05/2023 12:40'
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
         
        #Test with time outside the allowed range in the registered experiment
        data = {
            'user': str(self.reservation_1.user.pk),
            'experiment': str(self.reservation_1.experiment.pk),
            'start_datetime': '29/10/2023 13:00',
            'end_datetime': '29/10/2023 15:00'
        }
        response = self.client.post(self.reservation_view_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        expected_response_data = {'error': {'message': 'Reservation time exceeds experience time limit of ' + str(self.experiment_1.schedule_time)+ ' minutes'}}
        self.assertEqual(response.data, expected_response_data)
        
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(user=None)
        
    #PUT
    def test_reservation_PUT_without_authorization(self):
        '''
        This tests whether sending PUT request in reservation without authorization is not allowed
        '''
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'
        response = self.client.put(url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_reservation_PUT_without_permission(self):
        '''
        This tests whether sending PUT request in reservation without permission is not allowed
        '''
        expected_response_data = {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'
        self.client.force_authenticate(user=self.user_2)
        response = self.client.put(url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response_data)
        self.client.force_authenticate(user=None)
    
    def test_reservation_PUT(self):
        '''
        This tests whether sending PUT request in reservation with permission is successful
        '''
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'
        previous_reservation = self.reservation_1
        self.client.force_authenticate(user=self.user_1)
        
        response = self.client.put(url, self.update_data)
        
        updated_reservation = Reservation.objects.get(id = response.data['id'])
        data_is_equal = self.compare_data(model_to_dict(updated_reservation), response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(model_to_dict(previous_reservation), model_to_dict(updated_reservation))
        self.assertTrue(data_is_equal)
        
        self.client.force_authenticate(user=None)
    
    def test_reservation_PUT_without_data(self):
        '''
        This tests whether sending PUT request in reservation without data is not allowed
        ''' 
        self.client.force_authenticate(user=self.user_1)
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'        
        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.force_authenticate(user=None)
     
    
    def test_reservation_PUT_with_datetime_not_allowed(self):
        '''
        This tests whether it is not allowed to send a PUT request on reservation with existing datetime
        '''
        self.client.force_authenticate(user=self.user_1)        
        url = self.reservation_view_url + str(self.reservation_3.pk)+ '/'
        #Test with the same data in another reservation already registered
        data = {
            'user': str(self.user_1.pk),
            'experiment': str(self.reservation_3.experiment.pk),
            'start_datetime': self.change_br_format(self.reservation_2.start_datetime),
            'end_datetime': self.change_br_format(self.reservation_2.end_datetime)
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
     
        #Test with the date within the range of another reservation already registered
        data = {
            'user': str(self.user_1.pk),
            'experiment': str(self.reservation_3.experiment.pk),
            'start_datetime': '17/05/2023 12:22',
            'end_datetime': '17/05/2023 12:29',
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
          
        #Test with the start_datetime within the range of another reservation already registered
        data = {
            'user': str(self.user_1.pk),
            'experiment': str(self.reservation_3.experiment.pk),
            'start_datetime': '17/05/2023 12:22',
            'end_datetime': '17/05/2023 13:00'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        #Test with the end_datetime within the range of another reservation already registered
        data = {
            'user': str(self.user_1.pk),
            'experiment': str(self.reservation_3.experiment.pk),
            'start_datetime': '17/05/2023 12:00',
            'end_datetime': '17/05/2023 12:25'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        #Test with the start_datetime before and end_datetime after the range of another reservation already registered
        data = {
            'user': str(self.user_1.pk),
            'experiment': str(self.reservation_3.experiment.pk),
            'start_datetime': '17/05/2023 12:00',
            'end_datetime': '17/05/2023 12:40'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
         
        #Test with time outside the allowed range in the registered experiment
        data = {
            'user': str(self.user_1.pk),
            'experiment': str(self.reservation_3.experiment.pk),
            'start_datetime': '29/10/2023 13:00',
            'end_datetime': '29/10/2023 17:00'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_response_data = {'error': {'message': 'Reservation time exceeds experience time limit of ' + str(self.experiment_2.schedule_time)+ ' minutes'}}
        self.assertEqual(response.data, expected_response_data)
        
        self.client.force_authenticate(user=None)
       
    #PATCH
    def test_reservation_PATCH_without_authorization(self):
        '''
        This tests whether sending PATCH request in reservation without authorization is not allowed
        '''
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'
        response = self.client.patch(url, self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_reservation_PATCH_without_permission(self):
        '''
        This tests whether sending PATCH request in reservation without permission is not allowed
        '''
        expected_response_data = {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(url, self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response_data)
        self.client.force_authenticate(user=None)
    
   
    def test_reservation_PATCH(self):
        '''
        This tests whether sending PATCH request in reservation with permission is successful
        '''
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'
        previous_reservation = self.reservation_1
        self.client.force_authenticate(user=self.user_1)
        
        response = self.client.patch(url, data=self.patch_data)
        
        updated_reservation = Reservation.objects.get(id = self.reservation_1.pk)
        data_is_equal = self.compare_data(model_to_dict(updated_reservation), response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(model_to_dict(previous_reservation), model_to_dict(updated_reservation))
        self.assertTrue(data_is_equal)
        
        self.client.force_authenticate(user=None)
    
    
    def test_reservation_PATCH_with_datetime_not_allowed(self):
        '''    
        This tests whether it is not allowed to send a PATCH request on reservation with existing datetime
        '''
        self.client.force_authenticate(user=self.user_1)        
        url = self.reservation_view_url + str(self.reservation_3.pk)+ '/'
        
        #Test with the same data in another reservation already registered
        data = {
            'start_datetime': self.change_br_format(self.reservation_2.start_datetime),
            'end_datetime': self.change_br_format(self.reservation_2.end_datetime)
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        #Test with the date within the range of another reservation already registered
        data = {
            'start_datetime': '17/05/2023 12:22',
            'end_datetime': '17/05/2023 12:29',
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        #Test with the start_datetime within the range of another reservation already registered
        data = {
            'start_datetime': '17/05/2023 12:22'
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        #Test with the end_datetime within the range of another reservation already registered
        data = {
            'end_datetime': '17/05/2023 12:25'
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        #Test with time outside the allowed range in the registered experiment
        data = {
            'start_datetime': '17/05/2023 01:00'
        }
        response = self.client.patch(url, data=data)
        expected_response_data = {'error': {'message': 'Reservation time exceeds experience time limit of ' + str(self.experiment_2.schedule_time)+ ' minutes'}}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response_data)
        
        self.client.force_authenticate(user=None)
    
    #DELETE    
    def test_reservation_DELETE_without_authorization(self):
        '''
        This tests whether sending DELETE request in reservation without authorization is not allowed
        '''
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
    
    def test_reservation_DELETE_without_permission(self):
        '''
        This tests whether sending DELETE request in reservation without permission is not allowed
        '''
        self.client.force_authenticate(user=self.user_2)
        
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'
        response = self.client.delete(url)
        
        expected_response_data = {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response_data)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations)
        self.client.force_authenticate(user=None)
    
    def test_reservation_DELETE(self):
        '''
        This tests whether sending DELETE request in reservation with permission is successful
        '''
        self.client.force_authenticate(user=self.user_1)
        url = self.reservation_view_url + str(self.reservation_1.pk)+ '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.all().count(), self.amount_of_reservations - 1)
        self.client.force_authenticate(user=None)
    
    
    #Auxiliary functions
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
        res = self.change_date_format(date).strftime('%d/%m/%Y %H:%M')
        return res