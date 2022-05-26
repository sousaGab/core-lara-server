from django.db import models

class Experiment(models.Model):
    name =  models.CharField(max_length=30, blank=True)
    description = models.TextField(max_length=300, blank=True)
    type = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name