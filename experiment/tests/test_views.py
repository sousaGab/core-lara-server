from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from experiment.models import Experiment
import json

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
        
    def test_experiment_list_GET(self):
    
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
    
    def test_experiment_POST_without_authorization(self):
        
        response = self.client.post(self.list_url, {
            'name': 'Experiment_2', 
            'type':'Web',
            'description': 'Some Description',
            'location': 'Test Location', 
            'institution': 'Fantasy Institution'
        })
        
        self.assertEquals(response.status_code, 401)
        
    def test_experiment_POST(self):
        
        response = self.client.post(self.list_url, {
            'name': 'Experiment_2', 
            'type':'Web',
            'description': 'Some Description',
            'location': 'Test Location', 
            'institution': 'Fantasy Institution'
        })
        
        #print(response.data)
        #self.assertEquals(response.status_code, 302)
        #self.assertEquals(Experiment.objects.get_queryset(Experiment))
        
    
        