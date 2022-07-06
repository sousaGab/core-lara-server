from rest_framework.test import APITestCase
from reservation.models import Reservation

class TestReservationModel(APITestCase):
    
    def test_reservation(self):
        reservation = Reservation.objects.create(description='Test Reservation')
        self.assertEqual(str(reservation), 'Test Reservation')