from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from user.views import UserViewSet

class TestUrls(APITestCase):
    
    def setUp(self):
        self.list_url = reverse('Users-list')
        
    def test_list_url_resolves(self):
        self.assertEqual(resolve(self.list_url).func.__name__, UserViewSet.__name__)