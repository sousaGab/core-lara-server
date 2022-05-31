from django.db import models
from django.contrib.auth.models import User
from experiment.models import Experiment
from datetime import datetime
from django.db.models.fields import (
    DateField, DateTimeField, DurationField, Field, IntegerField, TimeField,
)
from django.utils import timezone

class Reservation(models.Model):
    
    user = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING,
        default=None,
        null=True,
        related_name='user'
    )
    experiment = models.ForeignKey(
        Experiment, 
        on_delete=models.DO_NOTHING,
        default=None,
        null=True,
        related_name='experiment'
    )
    time =  models.DateField(null=True, blank=True)
    description = models.TextField(
        max_length=300, 
        blank=True
    )
    
    def __str__(self):
        return self.description