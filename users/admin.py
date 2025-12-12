from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = (
		'id', 'username', 'email', 'is_course_admin', 'date_joined'
	)
	list_filter = ('is_course_admin', 'is_staff', 'is_superuser')
	search_fields = ('username', 'email')
