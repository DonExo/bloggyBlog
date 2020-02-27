from django.contrib import admin

from backend.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'is_staff']
    list_filter = ['is_staff']
    search_fields = ['first_name', 'last_name', 'email']


admin.site.register(User, UserAdmin)
