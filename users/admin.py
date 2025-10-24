from django.contrib import admin
from .models import UserProfile, UserPhoto

@admin.register(UserPhoto)
class UserPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_profile', 'image', 'is_main', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['user_profile__user__username', 'caption']
    readonly_fields = ['created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'city', 'age']
    list_filter = ['gender', 'city']
    search_fields = ['user__username', 'user__email', 'city']