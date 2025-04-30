from rest_framework import serializers
from .models import Category, Course, Module, Lesson
from users.serializers import UserLightSerializer
from reviews.serializers import ReviewSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = ['created_at']


class CourseSerializer(serializers.ModelSerializer):
    teacher = UserLightSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return avg if avg else 0

    def get_students_count(self, obj):
        return obj.enrollments.count()

    def create(self, validated_data):
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)