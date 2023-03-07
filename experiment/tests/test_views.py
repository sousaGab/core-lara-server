from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from django.urls import reverse
from experiment.models import Experiment
from django.contrib.auth.models import User
import json

'''
[X] GET 
[X] POST 
[X] PUT
[ ] PATCH
[ ] DELETE
'''
        

class TestViews(APITestCase):
    
    def setUp(self):
        
        self.client = APIClient()
        self.list_url = reverse('Experiments-list')
        self.experiment_1 = Experiment.objects.create(
            name= 'Experiment_1', 
            type='Web',
            description= 'Some Description',
            location= 'Test Location', 
            institution= 'Fantasy Institution'
        )
        self.normal_user = User.objects.create_user(
            username= 'normal_user',
            password='P4ssword@321'
        )
        self.admin_user = User.objects.create_superuser(
            username= 'admin_user',
            password='Admin@321'
        )
        self.amount_of_experiments = Experiment.objects.all().count()
        self.new_data = {
            'name': 'Experiment_2',
            'type':'Web',
            'description': 'Some Description',
            'location': 'Test Location', 
            'institution': 'Fantasy Institution'
        }
        self.update_data = {
            'name': 'Experiment_1',
            'type':'Physical',
            'description': 'Some Description',
            'location': 'Test Location', 
            'institution': 'Fantasy Institution'
        }
        
        
    #GET
    def test_experiment_list_GET(self):
        '''
        This will test if list request of experiment is successful
        '''
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    #POST
    def test_experiment_POST_without_authorization(self):
        '''
        This tests whether sending POST request in experiment without authorization is not allowed
        '''
        response = self.client.post(self.list_url, self.new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Experiment.objects.all().count(), self.amount_of_experiments)
    
    def test_experiment_POST_without_permission(self):
        '''
        This tests whether sending POST request in experiment without permission is not allowed
        '''
        self.client.force_authenticate(user=self.normal_user)
        
        response = self.client.post(self.list_url, self.new_data)
        
        expected_response_data = {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response_data)
        self.assertEqual(Experiment.objects.all().count(), self.amount_of_experiments)
        self.client.force_authenticate(user=None)
        
    def test_experiment_POST(self):
        '''
        This tests whether sending POST request in experiment with permission is successful
        '''
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.post(self.list_url, self.new_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experiment.objects.all().count(), self.amount_of_experiments + 1)
        self.client.force_authenticate(user=None)
    
    #PUT
    def test_experiment_PUT_without_authorization(self):
        '''
        This tests whether sending PUT request in experiment without authorization is not allowed
        '''
        url = self.list_url + str(self.experiment_1.pk)+ '/'
        response = self.client.put(url, data=self.update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_experiment_PUT_without_permission(self):
        '''
        This tests whether sending PUT request in experiment without permission is not allowed
        '''
        self.client.force_authenticate(user=self.normal_user)
        
        url = self.list_url + str(self.experiment_1.pk)+ '/'
        response = self.client.put(url, data=self.update_data)
        
        expected_response_data = {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response_data)
        self.client.force_authenticate(user=None)
        
    def test_experiment_PUT(self):
        '''
        This tests whether sending PUT request in experiment with permission is successful
        '''
        self.client.force_authenticate(user=self.admin_user)
        url = self.list_url + str(self.experiment_1.pk)+ '/'
        response = self.client.put(url, data=self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=None)
    
    #PATCH   
        
    