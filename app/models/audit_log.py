from django.db import models
from .user import User

class AuditLog(models.Model):
    class ActionType(models.TextChoices):
        LOGIN = 'LOGIN', 'Login'
        LOGOUT = 'LOGOUT', 'Logout'
        API_CALL = 'API_CALL', 'API Call'
        ROLE_CHANGE = 'ROLE_CHANGE', 'Role Change'
        USER_UPDATE = 'USER_UPDATE', 'User Update'
        USER_DELETE = 'USER_DELETE', 'User Delete'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=50, choices=ActionType.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    endpoint = models.CharField(max_length=255, blank=True)
    method = models.CharField(max_length=10, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True)  # in seconds
    details = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'audit_log'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

    @classmethod
    def log_action(cls, user, action, **kwargs):
        """Convenience method to log an action"""
        return cls.objects.create(user=user, action=action, **kwargs) 