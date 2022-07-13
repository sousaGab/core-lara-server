from rest_framework import viewsets
from rest_framework import permissions
from .models import Experiment
from .serializers import ExperimentSerializer
from .permissions import IsAdminOrReadOnly

class ExperimentViewSet (viewsets.ModelViewSet):
    
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = [IsAdminOrReadOnly]