from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet


router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('reviews/course/<int:course_id>/', ReviewViewSet.as_view({'get': 'course'}), name='reviews-by-course'),
    path('reviews/user/<int:user_id>/', ReviewViewSet.as_view({'get': 'user'}), name='reviews-by-user'),
]