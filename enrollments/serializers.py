from rest_framework import serializers
from django.utils import timezone
from .models import Enrollment, Progress
from courses.models import Lesson
from users.serializers import UserLightSerializer
from courses.serializers import CourseSerializer


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'

    def create(self, validated_data):
        if validated_data.get('is_completed', False):
            validated_data['completed_at'] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'is_completed' in validated_data and validated_data['is_completed'] and not instance.is_completed:
            validated_data['completed_at'] = timezone.now()
        return super().update(instance, validated_data)


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserLightSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    progress_summary = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['user', 'enrolled_at', 'completed_at']

    def get_progress_summary(self, obj):
        completed = Progress.objects.filter(enrollment=obj, is_completed=True).count()
        total = Lesson.objects.filter(module__course=obj.course).count()
        percentage = (completed / total * 100) if total > 0 else 0
        return {
            'completed_lessons': completed,
            'total_lessons': total,
            'percentage': round(percentage, 1)
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'is_completed' in validated_data and validated_data['is_completed'] and not instance.is_completed:
            validated_data['completed_at'] = timezone.now()
        return super().update(instance, validated_data)