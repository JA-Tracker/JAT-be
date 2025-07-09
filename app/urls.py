from django.urls import path
from .views.auth import LoginAPIView, RegisterAPIView, LogoutAPIView
from .views.profile import GetProfileAPIView, CreateProfileAPIView, UpdateProfileAPIView
from .views.admin import UserAdminViewSet, MonitoringView
from rest_framework_simplejwt.views import TokenRefreshView

# The API URLs
urlpatterns = [
    # Authentication URLs
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    # Profile URLs
    path('profile/', GetProfileAPIView.as_view(), name='get_profile'),
    path('profile/create/', CreateProfileAPIView.as_view(), name='create_profile'),
    path('profile/update/', UpdateProfileAPIView.as_view(), name='update_profile'),
    
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