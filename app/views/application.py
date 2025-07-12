from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import Application
from ..serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationUpdateSerializer
from ..utils.api import BaseAPIView, APIResponse

class ApplicationAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, application_id=None):
        """GET /applications/ - List all applications
           GET /applications/{id}/ - Get specific application"""
        try:
            if application_id:
                # Get specific application
                application = get_object_or_404(Application, id=application_id, user=request.user)
                serializer = ApplicationSerializer(application)
                return APIResponse.success(data=serializer.data)
            else:
                # Get all applications for user
                applications = Application.objects.filter(user=request.user)
                serializer = ApplicationSerializer(applications, many=True)
                return APIResponse.success(data=serializer.data)
        except Exception as e:
            return APIResponse.error(message="Failed to fetch applications")
    
    def post(self, request):
        """POST /applications/ - Create new application"""
        try:
            serializer_result = self.validate_serializer(
                ApplicationCreateSerializer, 
                request.data,
                context={'request': request}
            )
            
            if isinstance(serializer_result, ApplicationCreateSerializer):
                application = serializer_result.save()
                response_serializer = ApplicationSerializer(application)
                return APIResponse.success(data=response_serializer.data, status_code=status.HTTP_201_CREATED)
            else:
                return serializer_result
        except Exception as e:
            return APIResponse.error(message="Failed to create application")
    
    def put(self, request, application_id):
        """PUT /applications/{id}/ - Update specific application"""
        try:
            application = get_object_or_404(Application, id=application_id, user=request.user)
            serializer_result = self.validate_serializer(
                ApplicationUpdateSerializer,
                request.data,
                instance=application
            )
            
            if isinstance(serializer_result, ApplicationUpdateSerializer):
                updated_application = serializer_result.save()
                response_serializer = ApplicationSerializer(updated_application)
                return APIResponse.success(data=response_serializer.data)
            else:
                return serializer_result
        except Exception as e:
            return APIResponse.error(message="Failed to update application")
    
    def delete(self, request, application_id):
        """DELETE /applications/{id}/ - Delete specific application"""
        try:
            application = get_object_or_404(Application, id=application_id, user=request.user)
            application.delete()
            return APIResponse.success(message="Application deleted successfully")
        except Exception as e:
            return APIResponse.error(message="Failed to delete application")