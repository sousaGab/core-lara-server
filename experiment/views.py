from rest_framework import viewsets
from rest_framework import permissions
from experiment.models import Experiment
from experiment.serializers import ExperimentSerializer

class ExperimentViewSet (viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serialize_class = ExperimentSerializer
    permission_classes = [permissions.IsAuthenticated]