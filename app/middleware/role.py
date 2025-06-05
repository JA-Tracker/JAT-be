from django.http import JsonResponse
from rest_framework import status

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip middleware for non-authenticated users
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Define admin-only paths
        admin_paths = [
            '/api/admin/',
            '/api/users/',
            '/api/monitoring/'
        ]

        # Check if the request path starts with any admin path
        if any(request.path.startswith(path) for path in admin_paths):
            if not request.user.is_admin():
                return JsonResponse({
                    'error': 'You do not have permission to access this resource'
                }, status=status.HTTP_403_FORBIDDEN)

        return self.get_response(request) 