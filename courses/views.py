from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Course, Module, Lesson
from .serializers import CategorySerializer, CourseSerializer, LessonSerializer, ModuleSerializer
from django.shortcuts import get_object_or_404
from command.permissions import IsTeacher, IsCourseTeacherOrAdmin, IsEnrolledOrTeacherOrAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'teacher', 'is_published']
    ordering_fields = ['created_at', 'title', 'price']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsTeacher()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsCourseTeacherOrAdmin()]
        return [permissions.AllowAny()]

    @action(detail=False)
    def category(self, request, category_id=None):
        courses = self.queryset.filter(category_id=category_id, is_published=True)
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsCourseTeacherOrAdmin()]
        return [permissions.IsAuthenticated()]

    @action(detail=False)
    def course(self, request, course_id=None):
        modules = self.queryset.filter(course_id=course_id)
        page = self.paginate_queryset(modules)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(modules, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order']

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated(), IsEnrolledOrTeacherOrAdmin()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsCourseTeacherOrAdmin()]
        return [permissions.IsAuthenticated()]

    @action(detail=False)
    def module(self, request, module_id=None):
        module = get_object_or_404(Module, id=module_id)
        self.check_object_permissions(request, module)
        lessons = self.queryset.filter(module_id=module_id)
        page = self.paginate_queryset(lessons)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)