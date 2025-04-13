from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet, ProgressViewSet


router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'progress', ProgressViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
