from rest_framework import serializers
from .models import Category, Course, Module, Lesson


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'teacher', 'category',
            'price', 'discount_price', 'is_published', 'image',
            'created_at', 'updated_at'
        ]


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'course', 'title', 'description', 'order', 'created_at']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'module', 'title', 'content', 'video_url',
            'duration', 'order', 'created_at', 'updated_at'
        ]
