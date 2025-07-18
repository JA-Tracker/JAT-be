from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from app.models import User, AuditLog, Profile, Application
from app.mixins import ObjectManager, APIResponse, AuditMixin
from app.serializers.profile import ProfileSerializer
from app.serializers.application import ApplicationSerializer

class AdminUserManagementView(ObjectManager, AuditMixin):
    """Admin API for user management"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all users with their profiles"""
        # Check if user is admin
        if not request.user.is_admin():
            return APIResponse.error("Access denied. Admin privileges required.", status.HTTP_403_FORBIDDEN)
        
        users = User.objects.select_related('profile').all()
        
        user_data = []
        for user in users:
            user_info = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'profile': ProfileSerializer(user.profile).data if hasattr(user, 'profile') else None,
                'audit_logs_count': user.audit_logs.count(),
            }
            user_data.append(user_info)
        
        return APIResponse.success(data=user_data)
    
    def delete(self, request, user_id):
        """Delete a user"""
        if not request.user.is_admin():
            return APIResponse.error("Access denied. Admin privileges required.", status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return APIResponse.error("User not found", status.HTTP_404_NOT_FOUND)
        
        # Prevent admin from deleting themselves
        if user.id == request.user.id:
            return APIResponse.error("Cannot delete your own account", status.HTTP_400_BAD_REQUEST)
        
        username = user.username
        user.delete()
        
        # Log the deletion
        AuditLog.log_action(
            user=request.user,
            action=AuditLog.ActionType.USER_DELETE,
            details={'deleted_username': username, 'deleted_user_id': user_id}
        )
        
        return APIResponse.success(message="User deleted successfully")

class AdminAuditLogView(ObjectManager, AuditMixin):
    """Admin API for audit log monitoring"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get audit logs with filtering"""
        if not request.user.is_admin():
            return APIResponse.error("Access denied. Admin privileges required.", status.HTTP_403_FORBIDDEN)
        
        # Get query parameters
        user_id = request.GET.get('user_id')
        action = request.GET.get('action')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 50))
        
        # Build queryset
        queryset = AuditLog.objects.select_related('user').all()
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if action:
            queryset = queryset.filter(action=action)
        if start_date:
            queryset = queryset.filter(timestamp__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__date__lte=end_date)
        
        # Pagination
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        logs = queryset[start:end]
        
        # Format response
        log_data = []
        for log in logs:
            log_info = {
                'id': log.id,
                'user': {
                    'id': log.user.id,
                    'username': log.user.username,
                    'email': log.user.email,
                },
                'action': log.action,
                'timestamp': log.timestamp,
                'ip_address': log.ip_address,
                'endpoint': log.endpoint,
                'method': log.method,
                'status_code': log.status_code,
                'response_time': log.response_time,
                'details': log.details,
            }
            log_data.append(log_info)
        
        return APIResponse.success(data={
            'logs': log_data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': (total + page_size - 1) // page_size,
            }
        })

class AdminDashboardView(ObjectManager, AuditMixin):
    """Admin API for dashboard analytics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get dashboard statistics"""
        if not request.user.is_admin():
            return APIResponse.error("Access denied. Admin privileges required.", status.HTTP_403_FORBIDDEN)
        
        # Get date ranges
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # User statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
        new_users_month = User.objects.filter(date_joined__gte=month_ago).count()
        
        # API usage statistics
        api_calls_today = AuditLog.objects.filter(
            action=AuditLog.ActionType.API_CALL,
            timestamp__date=today
        ).count()
        
        api_calls_week = AuditLog.objects.filter(
            action=AuditLog.ActionType.API_CALL,
            timestamp__gte=week_ago
        ).count()
        
        # Top users by activity
        top_users = AuditLog.objects.values('user__username').annotate(
            activity_count=Count('id')
        ).order_by('-activity_count')[:10]
        
        # Recent activity
        recent_logs = AuditLog.objects.select_related('user').order_by('-timestamp')[:10]
        recent_activity = []
        for log in recent_logs:
            recent_activity.append({
                'user': log.user.username,
                'action': log.action,
                'timestamp': log.timestamp,
                'endpoint': log.endpoint,
            })
        
        # Action breakdown
        action_counts = AuditLog.objects.values('action').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return APIResponse.success(data={
            'users': {
                'total': total_users,
                'active': active_users,
                'new_week': new_users_week,
                'new_month': new_users_month,
            },
            'api_usage': {
                'today': api_calls_today,
                'week': api_calls_week,
            },
            'top_users': list(top_users),
            'recent_activity': recent_activity,
            'action_breakdown': list(action_counts),
        })

# URL patterns for admin views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_users(request):
    """Get all users"""
    view = AdminUserManagementView()
    return view.get(request)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_user(request, user_id):
    """Delete user"""
    view = AdminUserManagementView()
    return view.delete(request, user_id)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_audit_logs(request):
    """Get audit logs"""
    view = AdminAuditLogView()
    return view.get(request)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    """Get dashboard data"""
    view = AdminDashboardView()
    return view.get(request)

# --- NEW ADMIN ENDPOINTS ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_user_profile(request, user_id):
    """Admin: Get a user's profile by user_id"""
    if not request.user.is_admin():
        return APIResponse.error("Access denied. Admin privileges required.", status.HTTP_403_FORBIDDEN)
    try:
        profile = Profile.objects.get(user_id=user_id)
        return APIResponse.success(data=ProfileSerializer(profile).data)
    except Profile.DoesNotExist:
        return APIResponse.error("Profile not found", status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_user_applications(request, user_id):
    """Admin: Get all applications for a user"""
    if not request.user.is_admin():
        return APIResponse.error("Access denied. Admin privileges required.", status.HTTP_403_FORBIDDEN)
    applications = Application.objects.filter(user_id=user_id)
    data = ApplicationSerializer(applications, many=True).data
    return APIResponse.success(data=data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_application_detail(request, application_id):
    """Admin: Get a specific application by ID"""
    if not request.user.is_admin():
        return APIResponse.error("Access denied. Admin privileges required.", status.HTTP_403_FORBIDDEN)
    try:
        application = Application.objects.get(id=application_id)
        return APIResponse.success(data=ApplicationSerializer(application).data)
    except Application.DoesNotExist:
        return APIResponse.error("Application not found", status.HTTP_404_NOT_FOUND) 