from rest_framework import permissions
from enrollments.models import Enrollment


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher


class IsCourseTeacherOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'teacher'):
            return obj.teacher == request.user or request.user.is_staff
        elif hasattr(obj, 'course'):
            return obj.course.teacher == request.user or request.user.is_staff
        elif hasattr(obj, 'module'):
            return obj.module.course.teacher == request.user or request.user.is_staff
        return False


class IsEnrolledOrTeacherOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if hasattr(obj, 'module'):
            course = obj.module.course
        else:
            return False

        if course.teacher == request.user:
            return True

        return Enrollment.objects.filter(user=request.user, course=course).exists()


class IsEnrollmentOwnerOrTeacherOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.user == request.user:
            return True
        return obj.course.teacher == request.user


class IsProgressOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.enrollment.user == request.user


class IsReviewOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsEnrolledAndCompleted(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True

        course_id = request.data.get('course')
        if not course_id:
            return False

        return Enrollment.objects.filter(
            user=request.user,
            course_id=course_id,
            is_completed=True
        ).exists()