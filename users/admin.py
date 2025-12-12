from django.contrib import admin
from .models import User, ActivationCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'is_course_admin', 'date_joined'
    )
    list_filter = ('is_course_admin', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')


@admin.register(ActivationCode)
class ActivationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'used', 'attempts')
    list_filter = ('used', 'created_at')
    search_fields = ('user__username', 'code')
