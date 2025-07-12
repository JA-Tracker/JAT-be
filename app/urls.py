from django.urls import path
from .views.auth import LoginAPIView, RegisterAPIView, LogoutAPIView
from .views.profile import ProfileAPIView
from .views.application import ApplicationAPIView
from rest_framework_simplejwt.views import TokenRefreshView

# The API URLs
urlpatterns = [
    # Authentication URLs
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    # Profile URLs
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    
    # Application URLs
    path('applications/', ApplicationAPIView.as_view(), name='applications'),
    path('applications/<int:application_id>/', ApplicationAPIView.as_view(), name='application-detail'),
] 