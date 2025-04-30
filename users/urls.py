from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', lambda request: None, name='logout'),
    path('users/me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
]