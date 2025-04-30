from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'is_teacher', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_teacher', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('is_teacher', 'bio', 'profile_picture'),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('is_teacher', 'bio', 'profile_picture'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('-created_at',)
