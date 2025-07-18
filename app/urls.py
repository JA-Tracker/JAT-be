from django.urls import path
from .views.auth import LoginAPIView, RegisterAPIView, LogoutAPIView
from .views.profile import ProfileAPIView
from .views.application import ApplicationAPIView
from .views.application import ApplicationStatsAPIView
from .views.application import ApplicationAnalyticsAPIView
from .views.admin import (
    admin_users, admin_delete_user,
    admin_audit_logs, admin_dashboard,
    admin_user_profile, admin_user_applications, admin_application_detail
)
from rest_framework_simplejwt.views import TokenRefreshView

# The API URLs
urlpatterns = [
    # Authentication URLs
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    # Profile URLs
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    
    # Application URLs
    path('applications/', ApplicationAPIView.as_view(), name='applications'),
    path('applications/<int:application_id>/', ApplicationAPIView.as_view(), name='application-detail'),
    path('applications/stats/', ApplicationStatsAPIView.as_view(), name='application-stats'),
    path('applications/analytics/', ApplicationAnalyticsAPIView.as_view(), name='application-analytics'),
    
    # Admin URLs
    path('admin/users/', admin_users, name='admin-users'),
    path('admin/users/<int:user_id>/delete/', admin_delete_user, name='admin-delete-user'),
    path('admin/audit-logs/', admin_audit_logs, name='admin-audit-logs'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/users/<int:user_id>/profile/', admin_user_profile, name='admin-user-profile'),
    path('admin/users/<int:user_id>/applications/', admin_user_applications, name='admin-user-applications'),
    path('admin/applications/<int:application_id>/', admin_application_detail, name='admin-application-detail'),
] 