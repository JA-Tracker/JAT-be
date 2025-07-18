import time
from functools import wraps
from app.models import AuditLog

class AuditMixin:
    """
    Reusable mixin for auditing API calls
    """
    
    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to add audit logging"""
        start_time = time.time()
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Process the request
        response = super().dispatch(request, *args, **kwargs)
        
        # Log the API call if user is authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            response_time = time.time() - start_time
            
            # Determine action type
            action = AuditLog.ActionType.API_CALL
            if request.path.endswith('/login/') and request.method == 'POST':
                action = AuditLog.ActionType.LOGIN
            elif request.path.endswith('/logout/') and request.method == 'POST':
                action = AuditLog.ActionType.LOGOUT
            
            # Log the activity
            AuditLog.log_action(
                user=request.user,
                action=action,
                ip_address=ip,
                endpoint=request.path,
                method=request.method,
                status_code=response.status_code,
                response_time=response_time,
                details={
                    'query_params': dict(request.GET.items()),
                    'content_type': getattr(request, 'content_type', ''),
                }
            )
        
        return response

def audit_api_call(func):
    """
    Decorator for auditing API calls
    """
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        start_time = time.time()
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Process the request
        response = func(self, request, *args, **kwargs)
        
        # Log the API call if user is authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            response_time = time.time() - start_time
            
            # Determine action type
            action = AuditLog.ActionType.API_CALL
            if request.path.endswith('/login/') and request.method == 'POST':
                action = AuditLog.ActionType.LOGIN
            elif request.path.endswith('/logout/') and request.method == 'POST':
                action = AuditLog.ActionType.LOGOUT
            
            # Log the activity
            AuditLog.log_action(
                user=request.user,
                action=action,
                ip_address=ip,
                endpoint=request.path,
                method=request.method,
                status_code=response.status_code,
                response_time=response_time,
                details={
                    'query_params': dict(request.GET.items()),
                    'content_type': getattr(request, 'content_type', ''),
                }
            )
        
        return response
    return wrapper 