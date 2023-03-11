from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

'''
[X] GET
[ ] POST
[ ] PUT
[ ] PATCH
[ ] DELETE
'''

class TestViews(APITestCase):
    
    def setUp(self) :
        
        self.client = APIClient()
        self.list_url = reverse('Users-list')
        
        self.normal_user = User.objects.create_user(
            username= 'normal_user',
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
    
    #GET
    def test_user_list_GET_without_authorization(self):
        '''
        This will test if GET list request in user without authorization is not allowed
        '''
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_user_list_GET_without_permission(self):
        '''
        This will test if GET list request in user without permission is not allowed
        '''
        self.client.force_authenticate(user=self.normal_user)
        expected_response_data = {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response_data)
        self.client.force_authenticate(user=None)

    def test_user_list_GET(self):
        '''
        This will test if list request of user is successful
        '''
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=None)
    
    def test_user_GET_individual_without_authorization(self):
        '''
        This will test if GET request of individual user without authorization is not allowed
        '''
        url = self.list_url + str(self.normal_user.pk) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_user_GET_individual_without_permission(self):
        '''
        This will test if GET request of individual user without permission is not allowed
        '''
        self.client.force_authenticate(user=self.normal_user)
        url = self.list_url + str(self.user_2.pk) + '/'
        expected_response_data = {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response_data)
        self.client.force_authenticate(user=None)
    
    def test_user_GET_individual(self):
        '''
        This will test if GET request of individual user is successful
        '''
        self.client.force_authenticate(user=self.admin_user)
        url = self.list_url + str(self.normal_user.pk) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=None)
        
    #POST
    #PUT
    #PATCH
    #DELETE
    