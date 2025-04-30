from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from command.permissions import IsReviewOwner, IsEnrolledAndCompleted, IsOwnerOrAdmin
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at', 'rating']
    filterset_fields = ['rating']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsEnrolledAndCompleted()]
        elif self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsReviewOwner()]
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.AllowAny()]

    @action(detail=False)
    def course(self, request, course_id=None):
        reviews = self.queryset.filter(course_id=course_id)
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def user(self, request, user_id=None):
        if not (request.user.id == int(user_id) or request.user.is_staff):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        reviews = self.queryset.filter(user_id=user_id)
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)