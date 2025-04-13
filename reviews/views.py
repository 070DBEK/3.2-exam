from rest_framework.viewsets import ModelViewSet
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
