from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .api import APIResponse


class ObjectManager(APIView):
    """
    Base Object Manager with common error handling and response formatting
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
        context = kwargs.pop('context', {})
        context['request'] = self.request
        if instance:
            serializer = serializer_class(instance, data=data, partial=partial, context=context, **kwargs)
        else:
            serializer = serializer_class(data=data, context=context, **kwargs)
        
        if not serializer.is_valid():
            return APIResponse.error(
                message="Validation error",
                errors=serializer.errors
            )
        
        return serializer
