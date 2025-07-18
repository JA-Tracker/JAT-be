from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Profile
from ..serializers import ProfileSerializer, ProfileCreateUpdateSerializer
from ..mixins import ObjectManager, APIResponse
from ..mixins.audit import AuditMixin

class ProfileAPIView(ObjectManager, AuditMixin):
    """Profile API View - handles all profile CRUD operations"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """GET /profile/ - Get user's profile"""
        try:
            profile = request.user.profile
            serializer = ProfileSerializer(profile)
            return APIResponse.success(data=serializer.data)
        except Profile.DoesNotExist:
            return APIResponse.error(
                message="Profile not found. Please create a profile first.",
                status_code=status.HTTP_404_NOT_FOUND
            )
    
    def post(self, request):
        """POST /profile/ - Create new profile"""
        try:
            # Check if profile already exists
            if hasattr(request.user, 'profile'):
                return APIResponse.error(
                    message="Profile already exists",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            serializer_result = self.validate_serializer(ProfileCreateUpdateSerializer, request.data)
            
            if isinstance(serializer_result, ProfileCreateUpdateSerializer):
                profile = serializer_result.save()
                return APIResponse.success(
                    data=ProfileCreateUpdateSerializer(profile).data,
                    status_code=status.HTTP_201_CREATED
                )
            else:
                return serializer_result
                
        except Exception as e:
            return APIResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def put(self, request):
        """PUT /profile/ - Update user's profile"""
        try:
            profile = request.user.profile
            serializer_result = self.validate_serializer(
                ProfileCreateUpdateSerializer, 
                request.data, 
                instance=profile, 
                partial=True
            )
            
            if isinstance(serializer_result, ProfileCreateUpdateSerializer):
                updated_profile = serializer_result.save()
                return APIResponse.success(data=ProfileCreateUpdateSerializer(updated_profile).data)
            else:
                return serializer_result
                
        except Profile.DoesNotExist:
            return APIResponse.error(
                message="Profile not found. Please create a profile first.",
                status_code=status.HTTP_404_NOT_FOUND
            ) 