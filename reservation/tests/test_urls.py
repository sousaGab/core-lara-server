from rest_framework.reverse import reverse, reverse_lazy
from django.urls import resolve
from rest_framework.test import APITestCase
from reservation.views import ReservationViewSet

class TestUrls(APITestCase):
    
    def setUp(self):
        self.list_url = reverse('Reservations-list')
        
    def test_list_url_resolves(self):
        self.assertEqual(resolve(self.list_url).func.__name__, ReservationViewSet.__name__)

