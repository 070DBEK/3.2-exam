from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet, ProgressViewSet


router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'progress', ProgressViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('enrollments/user/<int:user_id>/', EnrollmentViewSet.as_view({'get': 'user'}), name='enrollments-by-user'),
    path('enrollments/course/<int:course_id>/', EnrollmentViewSet.as_view({'get': 'course'}),
         name='enrollments-by-course'),
    path('progress/enrollment/<int:enrollment_id>/', ProgressViewSet.as_view({'get': 'enrollment'}),
         name='progress-by-enrollment'),
]