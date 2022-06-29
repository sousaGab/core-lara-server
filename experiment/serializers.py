import this
from .models import Experiment
from rest_framework import serializers


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'