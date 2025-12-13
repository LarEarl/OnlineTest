from django.contrib import admin
from .models import Course, Module, Lesson


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'has_test')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_posted', 'created_at')
    list_filter = ('is_posted', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    date_hierarchy = 'created_at'


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [LessonInline]
    ordering = ('course', 'order')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'has_test', 'created_at')
    list_filter = ('module__course', 'module', 'has_test')
    search_fields = ('title', 'content')
    ordering = ('module', 'order')
    date_hierarchy = 'created_at'
