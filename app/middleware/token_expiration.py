from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse

class TokenExpirationMiddleware:
    """
    Middleware to check token expiration and handle expired tokens
    This runs on every request to check if the tokens are valid
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        # Only check on API routes to avoid unnecessary processing
        if request.path.startswith('/api/') and not request.path.startswith('/api/token/refresh/'):
            # Get the access token from cookies
            access_token = request.COOKIES.get('access')
            refresh_token = request.COOKIES.get('refresh')
            
            # If no tokens, just continue with the request
            if not access_token and not refresh_token:
                return self.get_response(request)
                
            # Check if both tokens exist
            if access_token and refresh_token:
                try:
                    # Validate the access token
                    self.jwt_auth.get_validated_token(access_token)
                    # Token is valid, continue with the request
                    return self.get_response(request)
                except (InvalidToken, TokenError):
                    # Access token is invalid, continue with the request
                    # The token will be refreshed by the frontend when it gets a 401
                    return self.get_response(request)
            elif refresh_token and not access_token:
                # If we only have a refresh token but no access token, 
                # we should not try to use it here - let the frontend handle it
                return self.get_response(request)
            
        # For all other requests, just continue
        response = self.get_response(request)
        return response 