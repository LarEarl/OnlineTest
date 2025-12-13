from django.contrib import admin
from .models import LessonProgress, ModuleProgress


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'lesson__module__course', 'completed_at')
    search_fields = ('user__email', 'user__username', 'lesson__title')
    readonly_fields = ('completed_at',)
    date_hierarchy = 'completed_at'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'lesson', 'lesson__module')


@admin.register(ModuleProgress)
class ModuleProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'is_unlocked', 'completed_lessons_count', 'completed_at')
    list_filter = ('is_unlocked', 'module__course', 'completed_at')
    search_fields = ('user__email', 'user__username', 'module__name')
    readonly_fields = ('completed_at',)
    date_hierarchy = 'completed_at'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'module', 'module__course')
