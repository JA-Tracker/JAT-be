from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import BaseViewSet
from .views.auth import register, login
from .views.profile import get_profile, create_profile, update_profile
from .views.admin import UserAdminViewSet, MonitoringView

# Create a router and register our viewsets with it
router = DefaultRouter()
# Example: router.register(r'items', ItemViewSet)
router.register(r'users', UserAdminViewSet, basename='user-admin')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    # Authentication URLs
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile URLs
    path('profile/', get_profile, name='get_profile'),
    path('profile/create/', create_profile, name='create_profile'),
    path('profile/update/', update_profile, name='update_profile'),
    
    # Admin Monitoring
    path('monitoring/', MonitoringView.as_view(), name='monitoring'),
] 