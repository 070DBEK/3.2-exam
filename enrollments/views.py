from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from command.permissions import (
    IsOwnerOrAdmin,
    IsEnrollmentOwnerOrTeacherOrAdmin,
    IsProgressOwner
)
from courses.models import Course
from .models import Enrollment, Progress
from .serializers import EnrollmentSerializer, ProgressSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_completed']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            return [permissions.IsAuthenticated(), IsEnrollmentOwnerOrTeacherOrAdmin()]
        elif self.action == 'list':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False)
    def user(self, request, user_id=None):
        if not (request.user.id == int(user_id) or request.user.is_staff):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        enrollments = self.queryset.filter(user_id=user_id)
        page = self.paginate_queryset(enrollments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def course(self, request, course_id=None):
        course = get_object_or_404(Course, id=course_id)
        if not (request.user.is_staff or course.teacher == request.user):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        enrollments = self.queryset.filter(course_id=course_id)
        page = self.paginate_queryset(enrollments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_completed']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsProgressOwner()]
        elif self.action == 'list':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False)
    def enrollment(self, request, enrollment_id=None):
        enrollment = get_object_or_404(Enrollment, id=enrollment_id)
        if not (request.user.is_staff or enrollment.user == request.user or enrollment.course.teacher == request.user):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        progress = self.queryset.filter(enrollment_id=enrollment_id)
        page = self.paginate_queryset(progress)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)