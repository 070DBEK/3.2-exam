from rest_framework import serializers
from .models import Enrollment, Progress


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at', 'is_completed', 'completed_at']


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'enrollment', 'lesson', 'is_completed', 'completed_at']
