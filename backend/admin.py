from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import User, Topic, Article


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff']
    search_fields = ['first_name', 'last_name', 'email']


class TopicAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'text', 'user', 'status']
    list_filter = ['status']
    search_fields = ['title', 'text', 'user']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Article, ArticleAdmin)

