from django.contrib import admin
from .models import Test, Question, AnswerOption, AnswerAttempt, CodeAttempt, CodeTestCase


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('text', 'is_code', 'order')


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 3
    fields = ('text', 'is_correct')


class CodeTestCaseInline(admin.TabularInline):
    model = CodeTestCase
    extra = 1
    fields = ('input_data', 'expected_output', 'time_limit')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'get_questions_count')
    list_filter = ('lesson__module__course', 'lesson__module')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    
    def get_questions_count(self, obj):
        return obj.questions.count()
    get_questions_count.short_description = 'Questions'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('get_short_text', 'test', 'is_code', 'order')
    list_filter = ('is_code', 'test__lesson__module__course')
    search_fields = ('text',)
    inlines = [AnswerOptionInline, CodeTestCaseInline]
    ordering = ('test', 'order')
    
    def get_short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    get_short_text.short_description = 'Question Text'
    
    def get_inlines(self, request, obj):
        if obj and obj.is_code:
            return [CodeTestCaseInline]
        return [AnswerOptionInline]


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__test__lesson__module__course')
    search_fields = ('text', 'question__text')


@admin.register(AnswerAttempt)
class AnswerAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at', 'question__test__lesson__module__course')
    search_fields = ('user__email', 'user__username', 'question__text')
    readonly_fields = ('user', 'question', 'selected_options', 'text_answer', 'is_correct', 'created_at')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False


@admin.register(CodeAttempt)
class CodeAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'status', 'is_correct', 'created_at', 'finished_at')
    list_filter = ('status', 'is_correct', 'created_at')
    search_fields = ('user__email', 'user__username', 'question__text')
    readonly_fields = ('user', 'question', 'code', 'status', 'is_correct', 'stdout', 'stderr', 'created_at', 'finished_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация', {
            'fields': ('user', 'question', 'created_at', 'finished_at')
        }),
        ('Код', {
            'fields': ('code', 'status', 'is_correct')
        }),
        ('Результат', {
            'fields': ('stdout', 'stderr'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False


@admin.register(CodeTestCase)
class CodeTestCaseAdmin(admin.ModelAdmin):
    list_display = ('question', 'get_short_input', 'get_short_output', 'time_limit')
    list_filter = ('question__test__lesson__module__course', 'time_limit')
    search_fields = ('question__text',)
    
    def get_short_input(self, obj):
        return obj.input_data[:30] + '...' if len(obj.input_data) > 30 else obj.input_data
    get_short_input.short_description = 'Input Data'
    
    def get_short_output(self, obj):
        return obj.expected_output[:30] + '...' if len(obj.expected_output) > 30 else obj.expected_output
    get_short_output.short_description = 'Expected Output'
