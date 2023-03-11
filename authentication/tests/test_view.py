from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.urls import reverse
import json

class TestViews(APITestCase):
    
    def setUp(self):
        
        self.client = APIClient()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.token_verify_url = reverse('token_verify')
        self.token_refresh_url = reverse('token_refresh')
        
        self.user = User.objects.create_user(
            username= 'example',
            password='P4ssword@321'
        )

    def test_login(self):
        '''
        This will test successful login
        '''
        
        data = {
            'username' : 'example',
            'password' : 'P4ssword@321'
        }
        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_login_error(self):
        '''
        This will test if logging in with incorrect data returns an error
        '''
        
        data = {
            'username' : 'example',
            'password' : 'wrong_password'
        }
        response = self.client.post(self.login_url, data=data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid password'})
        
        response = self.client.post(self.login_url, data={}) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register(self):
        '''
        This will test successful register
        '''
        
        data = {
            'username': 'example_test',
            'name': 'user',
            'email': 'email@test.com.com',
            'location': 'Some Address here',
            'birth_date': '01/01/2000',
            'password': 'P4ssword@321'
        }
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(User.objects.get(username = data['username']))
        
    def test_register_without_data(self):
        '''
        This will test if an error is returned when performing the registration without data
        '''
        
        data = {}
        amount_of_users = User.objects.all().count()
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), amount_of_users)
        
    def test_token_verify(self):
        '''
        This test if the Token verification is successful
        '''
        
        data = {
            'username' : 'example',
            'password' : 'P4ssword@321'
        }
        login_response = self.client.post(self.login_url, data=data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        token = login_response.data['data']['access_token']
        data = {
            'token' : token
        }
        response = self.client.post(self.token_verify_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_token_verify_with_wrong_data(self):
        '''
        This will test if an error is returned when performing verify token with wrong data
        '''
        
        token = 'WrongTOKEN'
        data = {
            'token' : token
        }
        response = self.client.post(self.token_verify_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_token_refresh(self):
        '''
        This test if the Token refresh is successful
        '''
        
        data = {
            'username' : 'example',
            'password' : 'P4ssword@321'
        }
        login_response = self.client.post(self.login_url, data=data)    
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        refresh_token = login_response.data['data']['refresh_token']
        data = {
            'refresh' : refresh_token
        }
        response = self.client.post(self.token_refresh_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access_token = response.data['access']
        data = {
            'token' : access_token
        }
        response = self.client.post(self.token_verify_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_token_refresh_with_wrong_data(self):
        '''
        This will test if an error is returned when performing refresh token with wrong data
        '''
        
        token = 'WrongTOKEN'
        data = {
            'refresh' : token
        }
        response = self.client.post(self.token_refresh_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   
        
    #def test_logout(self):
        '''
        This will test successful logout
        '''
        #self.token = Token.objects.get(user=self.user)
        #self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        #response = self.client.post(self.login_url)
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        