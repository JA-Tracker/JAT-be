from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from ..models import User, Profile
from ..serializers import UserSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only admins can see all users
        user = self.request.user
        if user.is_admin():
            return User.objects.all()
        return User.objects.none()

    @action(detail=True, methods=['post'])
    def set_role(self, request, pk=None):
        user = self.get_object()
        role = request.data.get('role')
        if role not in ['ADMIN', 'USER']:
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        user.role = role
        user.save()
        return Response({'status': 'role set', 'role': user.role})

    @action(detail=True, methods=['delete'])
    def delete_user(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response({'status': 'user deleted'})

# Monitoring actions can be implemented here as needed
class MonitoringView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if user is admin
        if not request.user.is_admin():
            return Response({"error": "You do not have permission to access this resource"}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        # Get time ranges
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)
        last_30d = now - timedelta(days=30)
        
        # Calculate user stats
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        admins = User.objects.filter(role=User.Role.ADMIN).count()
        
        # Recent user activity
        recent_logins = User.objects.filter(last_login__gte=last_24h).count()
        
        # New users
        new_users_24h = User.objects.filter(date_joined__gte=last_24h).count()
        new_users_7d = User.objects.filter(date_joined__gte=last_7d).count()
        new_users_30d = User.objects.filter(date_joined__gte=last_30d).count()
        
        # User roles distribution
        roles_distribution = User.objects.values('role').annotate(count=Count('id'))
        
        # Token information
        active_tokens = OutstandingToken.objects.filter(expires_at__gt=now).count()
        blacklisted_tokens = BlacklistedToken.objects.count()
        
        # Get the 5 most recently active users
        recent_active_users = User.objects.filter(last_login__isnull=False).order_by('-last_login')[:5]
        recent_active_data = []
        for user in recent_active_users:
            recent_active_data.append({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'last_login': user.last_login,
                'role': user.role
            })
        
        # Get the 5 newest users
        newest_users = User.objects.order_by('-date_joined')[:5]
        newest_users_data = []
        for user in newest_users:
            newest_users_data.append({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'date_joined': user.date_joined,
                'role': user.role
            })
        
        # Profiles stats
        profiles_count = Profile.objects.count()
        profiles_complete = Profile.objects.filter(
            ~Q(bio='') | ~Q(location='') | ~Q(birth_date__isnull=True) | ~Q(avatar='')
        ).count()
        
        return Response({
            'user_stats': {
                'total_users': total_users,
                'active_users': active_users,
                'admin_users': admins,
                'recent_logins_24h': recent_logins,
                'new_users': {
                    'last_24h': new_users_24h,
                    'last_7d': new_users_7d,
                    'last_30d': new_users_30d
                },
                'roles_distribution': roles_distribution
            },
            'token_stats': {
                'active_tokens': active_tokens,
                'blacklisted_tokens': blacklisted_tokens
            },
            'recent_active_users': recent_active_data,
            'newest_users': newest_users_data,
            'profile_stats': {
                'total_profiles': profiles_count,
                'completed_profiles': profiles_complete,
                'completion_rate': round((profiles_complete / profiles_count * 100) if profiles_count > 0 else 0, 2)
            }
        }) 