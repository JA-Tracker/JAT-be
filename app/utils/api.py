from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction

class APIResponse:
    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        """
        Create a standardized success response
        """
        response_data = {}
        if data is not None:
            response_data['data'] = data
        if message is not None:
            response_data['message'] = message
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message, status_code=status.HTTP_400_BAD_REQUEST, errors=None):
        """
        Create a standardized error response
        """
        response_data = {'error': message}
        if errors is not None:
            response_data['details'] = errors
        return Response(response_data, status=status_code)

class BaseAPIView(APIView):
    """
    Base API View with common error handling and response formatting
    """
    permission_classes = [IsAuthenticated]  # Default permission
    
    def handle_exception(self, exc):
        """
        Handle exceptions and return standardized error responses
        """
        if hasattr(exc, 'detail'):
            # DRF exceptions
            return APIResponse.error(
                message=str(exc),
                status_code=exc.status_code if hasattr(exc, 'status_code') else status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors=exc.detail if hasattr(exc, 'detail') else None
            )
        
        # Generic exceptions
        return APIResponse.error(
            message=str(exc),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    def validate_serializer(self, serializer_class, data, instance=None, partial=False, **kwargs):
        """
        Validate serializer data and return serializer or error response
        """
        if instance:
            serializer = serializer_class(instance, data=data, partial=partial, **kwargs)
        else:
            serializer = serializer_class(data=data, **kwargs)
            
        if not serializer.is_valid():
            return APIResponse.error(
                message="Validation error",
                errors=serializer.errors
            )
        
        return serializer 