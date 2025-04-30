from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'course')
    search_fields = ('user__username', 'course__title', 'comment')
    autocomplete_fields = ('user', 'course')
