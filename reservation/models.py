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
        on_delete=models.CASCADE,
        default=None,
        null=False,
        related_name='user'
    )
    experiment = models.ForeignKey(
        Experiment, 
        on_delete=models.CASCADE,
        default=None,
        null=False,
        related_name='experiment'
    )
    start_datetime = models.DateTimeField(null=False, blank=False)
    end_datetime = models.DateTimeField(null=False, blank=False)
    showed_up = models.BooleanField(null=True, default=False)
    finished = models.BooleanField(null=True, default=False)
    description = models.TextField(
        max_length=300, 
        blank=True
    )
    
    def __str__(self):
        #initial_datetime = "(start:%s"% self.start_datetime.strftime('%m/%d/%Y %H:%M')
        #finish_datetime = ",end:%s)"%  self.end_datetime.strftime('%m/%d/%Y %H:%M')
        #return  initial_datetime + finish_datetime
        return str(self.id)