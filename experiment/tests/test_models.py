from rest_framework.test import APITestCase
from experiment.models import Experiment

class TestModel(APITestCase):
    
    def test_experiment(self):
        experiment = Experiment.objects.create(name='Test Experiment')
        self.assertEqual(str(experiment), 'Test Experiment')