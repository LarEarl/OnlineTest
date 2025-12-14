from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services import complete_lesson
from courses.models import *

@login_required
def my_progress(request):
    """Страница с прогрессом пользователя"""
    from .models import LessonProgress, ModuleProgress
    from courses.models import Course
    
    user = request.user
    
    # Проверяем, есть ли информация о завершенном курсе (только один раз!)
    completed_course_id = request.session.pop('completed_course_id', None)
    completed_course_data = request.session.pop('completed_course_data', {})
    completed_course_obj = None
    if completed_course_id:
        # Явно сохраняем изменения в сессии
        request.session.modified = True
        try:
            completed_course_obj = Course.objects.get(id=completed_course_id)
        except Course.DoesNotExist:
            pass
    
    # Получаем все курсы
    courses = Course.objects.filter(is_posted=True)
    
    progress_data = []
    for course in courses:
        modules = course.modules.all()
        total_lessons = sum(module.lessons.count() for module in modules)
        completed_lessons = LessonProgress.objects.filter(
            user=user,
            lesson__module__course=course,
            is_completed=True
        ).count()
        
        if total_lessons > 0:
            progress_percent = int((completed_lessons / total_lessons) * 100)
        else:
            progress_percent = 0
        
        progress_data.append({
            'course': course,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percent': progress_percent
        })
    
    # Последние завершенные уроки
    recent_lessons = LessonProgress.objects.filter(
        user=user,
        is_completed=True
    ).select_related('lesson__module__course').order_by('-completed_at')[:5]
    
    return render(request, 'progress/my_progress.html', {
        'title': 'Мой прогресс',
        'progress_data': progress_data,
        'recent_lessons': recent_lessons,
        'completed_course': completed_course_obj,
        'completed_course_data': completed_course_data
    })

@login_required
def complete_lesson_view(request, lesson_id):
    """Завершение урока"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    result = complete_lesson(request.user, lesson)
    
    messages.success(request, f'Урок "{lesson.title}" завершен!')
    
    # Если курс завершен, сохраняем это в сессии для показа достижения
    if result.get('course_completed'):
        request.session['completed_course_id'] = result.get('course_id')
        request.session['completed_course_data'] = {
            'xp_gained': result.get('xp_gained', 100),
            'level_up': result.get('level_up', False),
            'new_level': result.get('new_level', 0)
        }
        return redirect('progress:my_progress')
    
    return redirect('courses:lessons', modul_slug=lesson.module.slug)