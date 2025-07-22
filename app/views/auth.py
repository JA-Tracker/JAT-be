from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib.auth import authenticate
from ..models import User
from ..serializers import UserSerializer, UserCreateSerializer
from ..mixins import ObjectManager, APIResponse, AuditMixin

class AuthenticationAPIView(ObjectManager, AuditMixin):
    """Base class for authentication related views"""
    permission_classes = [AllowAny]

class RegisterAPIView(AuthenticationAPIView):
    def post(self, request):
        serializer_result = self.validate_serializer(UserCreateSerializer, request.data)
        
        if isinstance(serializer_result, UserCreateSerializer):
            user = serializer_result.save()
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            cookies = [
                {
                    'key': 'refresh',
                    'value': str(refresh),
                    'httponly': True,
                    'secure': True,
                    'samesite': 'None',
                },
                {
                    'key': 'access',
                    'value': str(access),
                    'httponly': True,
                    'secure': True,
                    'samesite': 'None',
                }
            ]
            return APIResponse.success(
                data={
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(access),
                    }
                },
                status_code=status.HTTP_201_CREATED,
                cookies=cookies
            )
        else:
            # If validation failed, serializer_result is already an error response
            return serializer_result

class LoginAPIView(AuthenticationAPIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return APIResponse.error(
                message="Please provide both email and password",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(email=email, password=password)

        if not user:
            return APIResponse.error(
                message="Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        cookies = [
            {
                'key': 'refresh',
                'value': str(refresh),
                'httponly': True,
                'secure': True,
                'samesite': 'None',
            },
            {
                'key': 'access',
                'value': str(access),
                'httponly': True,
                'secure': True,
                'samesite': 'None',
            }
        ]
        return APIResponse.success(
            data={
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(access),
                }
            },
            status_code=status.HTTP_200_OK,
            cookies=cookies
        )


class LogoutAPIView(ObjectManager, AuditMixin):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return APIResponse.error(
                    message="Refresh token is required",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
            token = RefreshToken(refresh_token)
            token.blacklist()
            # Clear cookies by setting them to empty and expired
            cookies = [
                {
                    'key': 'refresh',
                    'value': '',
                    'httponly': True,
                    'secure': True,
                    'samesite': 'None',
                    'expires': 0,
                },
                {
                    'key': 'access',
                    'value': '',
                    'httponly': True,
                    'secure': True,
                    'samesite': 'None',
                    'expires': 0,
                }
            ]
            return APIResponse.success(
                message="User logged out successfully",
                status_code=status.HTTP_200_OK,
                cookies=cookies
            )
        except Exception as e:
            return APIResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            ) 