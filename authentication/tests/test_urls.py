from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from authentication.views import LoginAPIView, RegisterAPIView
from rest_framework_simplejwt import views as jwt_views

class TestUrls(APITestCase):

    def setUp(self):
    
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.token_verify_url = reverse('token_verify')
        self.token_refresh_url = reverse('token_refresh')
        
    def test_list_url_resolves(self):
        
        self.assertEquals(resolve(self.login_url).func.__name__, LoginAPIView.__name__)
        self.assertEquals(resolve(self.register_url).func.__name__, RegisterAPIView.__name__)
        self.assertEquals(resolve(self.token_verify_url).func.__name__, jwt_views.TokenVerifyView.__name__)
        self.assertEquals(resolve(self.token_refresh_url).func.__name__, jwt_views.TokenRefreshView.__name__)
