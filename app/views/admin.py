from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import User
from ..serializers import UserSerializer

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
from rest_framework.views import APIView

class MonitoringView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Example: return a list of user actions (stub)
        return Response({'actions': ['login', 'logout', 'profile_update']}) 