from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Profile
from ..serializers import ProfileSerializer
from ..utils.api import BaseAPIView, APIResponse

class ProfileAPIView(BaseAPIView):
    """Base class for profile related views"""
    permission_classes = [IsAuthenticated]

class GetProfileAPIView(ProfileAPIView):
    def get(self, request):
        try:
            profile = request.user.profile
            serializer = ProfileSerializer(profile)
            return APIResponse.success(data=serializer.data)
        except Profile.DoesNotExist:
            return APIResponse.error(
                message="Profile not found. Please create a profile first.",
                status_code=status.HTTP_404_NOT_FOUND
            )

class CreateProfileAPIView(ProfileAPIView):
    def post(self, request):
        try:
            # Check if profile already exists
            if hasattr(request.user, 'profile'):
                return APIResponse.error(
                    message="Profile already exists",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            serializer_result = self.validate_serializer(ProfileSerializer, request.data)
            
            if isinstance(serializer_result, ProfileSerializer):
                profile = serializer_result.save(user=request.user)
                return APIResponse.success(
                    data=ProfileSerializer(profile).data,
                    status_code=status.HTTP_201_CREATED
                )
            else:
                # If validation failed, serializer_result is already an error response
                return serializer_result
                
        except Exception as e:
            return APIResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

class UpdateProfileAPIView(ProfileAPIView):
    def put(self, request):
        try:
            profile = request.user.profile
            serializer_result = self.validate_serializer(
                ProfileSerializer, 
                request.data, 
                instance=profile, 
                partial=True
            )
            
            if isinstance(serializer_result, ProfileSerializer):
                updated_profile = serializer_result.save()
                return APIResponse.success(data=ProfileSerializer(updated_profile).data)
            else:
                # If validation failed, serializer_result is already an error response
                return serializer_result
                
        except Profile.DoesNotExist:
            return APIResponse.error(
                message="Profile not found. Please create a profile first.",
                status_code=status.HTTP_404_NOT_FOUND
            ) 