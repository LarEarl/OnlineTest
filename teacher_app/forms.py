from django import forms
from courses.models import Course, Module, Lesson
from tests_app.models import Test, Question, AnswerOption


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'slug', 'is_posted']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Python для начинающих'}),
            'description': forms.Textarea(attrs={'placeholder': 'Полный вводный курс по Python'}),
            'slug': forms.TextInput(attrs={'placeholder': 'python-novice'}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['course', 'name', 'description', 'slug', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введение в Python'}),
            'description': forms.Textarea(attrs={'placeholder': 'Что такое Python и зачем он нужен'}),
            'slug': forms.TextInput(attrs={'placeholder': 'vvedenie-v-python'}),
            'order': forms.NumberInput(attrs={'min': 1, 'value': 1}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['module', 'title', 'content', 'video_url', 'order', 'has_test']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Первая программа Hello World'}),
            'content': forms.Textarea(attrs={'placeholder': 'print("Hello, World!")'}),
            'video_url': forms.TextInput(attrs={'placeholder': 'https://youtu.be/...'}),
            'order': forms.NumberInput(attrs={'min': 1, 'value': 1}),
        }


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['lesson', 'title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Тест по установке Python'}),
            'description': forms.Textarea(attrs={'placeholder': 'Проверьте знания после урока'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['test', 'text', 'is_code', 'order']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Как проверить версию Python?'}),
            'order': forms.NumberInput(attrs={'min': 1, 'value': 1}),
        }


class QuestionEditForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'is_code', 'order']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Текст вопроса', 'rows': 3}),
            'order': forms.NumberInput(attrs={'min': 1}),
        }


class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ['question', 'text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'python --version'}),
        }


class AnswerOptionEditForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Текст ответа'}),
        }
