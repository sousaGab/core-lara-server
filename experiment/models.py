from django.db import models
from model_utils import Choices

class Experiment(models.Model):
    TYPES = Choices(
        ('Physical', 'Physical'),
        ('Web', 'Web')
    )
    name = models.CharField(max_length=30, blank=False)
    type = models.CharField(max_length=30, choices=TYPES, default=TYPES.Physical)
    description = models.TextField(max_length=300, blank=True)
    location = models.CharField(max_length=120, blank=True)
    institution = models.CharField(max_length=120, default='UESB')

    def __str__(self): return self.name