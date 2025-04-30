from django.contrib import admin
from .models import Enrollment, Progress


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'enrolled_at')
    search_fields = ('user__username', 'course__title')
    autocomplete_fields = ('user', 'course')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed',)
    search_fields = ('enrollment__user__username', 'lesson__title')
    autocomplete_fields = ('enrollment', 'lesson')
