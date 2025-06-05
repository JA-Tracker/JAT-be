from django.contrib import admin
from ..models import User, Profile

class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(User)
class UserAdmin(BaseModelAdmin):
    list_display = ('id', 'email', 'username', 'role', 'is_active', 'created_at')
    search_fields = ('email', 'username', 'role')
    list_filter = ('role', 'is_active')

@admin.register(Profile)
class ProfileAdmin(BaseModelAdmin):
    list_display = ('id', 'user', 'bio', 'location', 'birth_date', 'created_at')
    search_fields = ('user__email', 'user__username', 'location') 