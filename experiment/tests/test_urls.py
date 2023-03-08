from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from experiment.views import ExperimentViewSet


class TestUrls(APITestCase):

    def setUp(self):
    
        self.list_url = reverse('Experiments-list')
        
    def test_list_url_resolves(self):
        self.assertEqual(resolve(self.list_url).func.__name__, ExperimentViewSet.__name__)