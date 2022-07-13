import this
from .models import Experiment
from rest_framework import serializers


class ExperimentSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=Experiment.TYPES)
    
    class Meta:
        model = Experiment
        fields = '__all__'