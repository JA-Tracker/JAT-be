from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.models import User, AuditLog, Profile, Application

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False 