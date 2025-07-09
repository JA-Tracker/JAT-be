from django.urls import path
from .views.auth import register, login, logout
from .views.profile import get_profile, create_profile, update_profile
from .views.admin import UserAdminViewSet, MonitoringView
from rest_framework_simplejwt.views import TokenRefreshView

# The API URLs
urlpatterns = [
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout, name='logout'),
    
    # Profile URLs
    path('profile/', get_profile, name='get_profile'),
    path('profile/create/', create_profile, name='create_profile'),
    path('profile/update/', update_profile, name='update_profile'),
    
    # Admin URLs
    path('admin/users/', UserAdminViewSet.as_view({
        'get': 'list', 'post': 'create'
        })
        , name='user-admin-list'),
    path('admin/users/<int:pk>/', UserAdminViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
        })
        , name='user-admin-detail'),
    path('admin/users/<int:pk>/set_role/', UserAdminViewSet.as_view({
        'post': 'set_role'
        })
        , name='user-admin-set-role'),
    path('admin/users/<int:pk>/delete_user/', UserAdminViewSet.as_view({
        'delete': 'delete_user'
        })
        , name='user-admin-delete-user'),
    
    # Admin Monitoring
    path('admin/monitoring/', MonitoringView.as_view(), name='monitoring'),
] 