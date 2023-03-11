from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import Profile
from django.forms.models import model_to_dict

'''
[X] GET
[X] POST
[ ] PUT
[ ] PATCH
[ ] DELETE
'''

class TestViews(APITestCase):
    
    def setUp(self) :
        
        self.client = APIClient()
        self.list_url = reverse('Users-list')
        
        # create user
        self.normal_user = User.objects.create_user(
            username= 'normal_user',
            password='P4ssword@321'
        )
        # adjust profile
        self.profile_1 = Profile.objects.get(user=self.normal_user)
        self.profile_1.name = 'user'
        self.profile_1.email = 'email@test.com.com'
        self.profile_1.location = 'Some Address here'
        self.profile_1.birth_date = '2000-01-01'
        self.profile_1.save()
        
        
        
        # create user
        self.user_2 = User.objects.create_user(
            username= 'user_2',
            password='P4ssword@321'
        )
        # adjust profile
        self.profile_2 = Profile.objects.get(user=self.normal_user)
        self.profile_2.name = 'user_2'
        self.profile_2.email = 'email2@test.com.com'
        self.profile_2.location = 'Some Address here'
        self.profile_2.birth_date = '2000-02-02'
        self.profile_2.save()
        
        self.admin_user = User.objects.create_superuser(
            username= 'admin_user',
            password='Admin@321'
        )
        
        self.new_data = {
            'username': 'example_test',
            'name': 'user',
            'email': 'email@test.com.com',
            'location': 'Some Address here',
            'birth_date': '01/01/2000',
            'password': 'P4ssword@321'
        }
        
        self.update_data = {
            'username': 'new_username',
            'name': 'user_updated',
            'email': 'emailupdated@test.com.com',
            'location': 'Some Address there',
            'birth_date': '01/01/2000'
        }
        
    
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
    def test_user_POST_is_not_allowed(self):
        '''
        This tests whether sending POST request in user is not allowed
        '''
        # This request is not allowed because users are created using registration request
        response = self.client.post(self.list_url, self.new_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    #PUT
    def test_user_PUT_without_authorization(self):
        '''
        This tests whether sending PUT request in user without authorization is not allowed
        '''
        url = self.list_url + str(self.user_2.pk) + '/'
        response = self.client.put(url, data = self.update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_PUT_without_permission(self):
        '''
        This tests whether sending PUT request in user without permission is not allowed
        '''
        self.client.force_authenticate(user=self.normal_user)
        url = self.list_url + str(self.user_2.pk) + '/'
        expected_response_data = {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}
        response = self.client.put(url, data = self.update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_response_data)
        self.client.force_authenticate(user=None)
        
    def test_user_PUT(self):
        '''
        This tests whether sending PUT request iin user with permission is successful
        '''
        self.client.force_authenticate(user=self.normal_user)
        previous_profile = self.profile_1
        url = self.list_url + str(self.normal_user.pk) + '/'
        response = self.client.put(url, data = self.update_data)
        updated_profile = Profile.objects.get(user = self.normal_user)
        data_is_equal = self.compare_data(model_to_dict(updated_profile), response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(model_to_dict(previous_profile), model_to_dict(updated_profile))
        self.assertTrue(data_is_equal)
        self.client.force_authenticate(user=None)
        
    #PATCH
    #DELETE
    
    
    #Auxiliary functions
    def compare_data(self, data_1, data_2):
        
        keys = ['id', 'username', 'name', 'location', 'email', 'birth_date']    
        for key in keys:
            
            if key == 'birth_date':
                datetime_1 = self.change_date_format(str(data_1[key])) 
                datetime_2 = self.change_date_format(str(data_2[key]))
                if datetime_1  != datetime_2 : return False
            else :
                if data_1[key] != data_2[key] :
                    return False
                
        return True
    
    def change_date_format(self, date):
        res = datetime.strptime(date, '%Y-%m-%d')
        return res
    