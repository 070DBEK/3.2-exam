from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    CourseViewSet,
    ModuleViewSet,
    LessonViewSet
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'lessons', LessonViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('courses/category/<int:category_id>/', CourseViewSet.as_view({'get': 'category'}), name='courses-by-category'),
    path('modules/course/<int:course_id>/', ModuleViewSet.as_view({'get': 'course'}), name='modules-by-course'),
    path('lessons/module/<int:module_id>/', LessonViewSet.as_view({'get': 'module'}), name='lessons-by-module'),
]