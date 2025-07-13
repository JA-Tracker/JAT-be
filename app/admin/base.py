from django.contrib import admin
from ..models import User, Profile

class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('id',)
    readonly_fields = ()

@admin.register(User)
class UserAdmin(BaseModelAdmin):
    list_display = ('id', 'email', 'username', 'role', 'is_active', 'date_joined')
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('email', 'username', 'role')
    list_filter = ('role', 'is_active')
    ordering = ('-date_joined',)

@admin.register(Profile)
class ProfileAdmin(BaseModelAdmin):
    list_display = ('id', 'user', 'first_name', 'middle_name', 'last_name', 'birth_date')
    search_fields = ('user__email', 'user__username', 'first_name', 'middle_name', 'last_name') 