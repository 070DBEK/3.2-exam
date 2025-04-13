from rest_framework.viewsets import ModelViewSet
from .models import Enrollment, Progress
from .serializers import EnrollmentSerializer, ProgressSerializer


class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class ProgressViewSet(ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
