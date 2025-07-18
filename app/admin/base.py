from django.contrib import admin

class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('id',)
    readonly_fields = ()