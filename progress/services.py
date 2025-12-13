from datetime import datetime
from courses.models import Module, Lesson, Course
from .models import LessonProgress, ModuleProgress
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now




def get_all_open_modules(user, course: Course):
    modules = course.modules.order_by('order')
    open_modules = []

    for module in modules:
        progress, _ = ModuleProgress.objects.get_or_create(
            user=user,
            module=module
        )

        open_modules.append({
            'module': module,
            'progress': progress,
            'is_open': progress.is_unlocked or module.order == 0
        })

        if not progress.is_unlocked and module.order != 1:
            break

    return open_modules



def get_all_open_lessons(user, module: Module):
    lessons = module.lessons.order_by('order')
    open_lessons = []

    for lesson in lessons:
        progress, _ = LessonProgress.objects.get_or_create(
            user=user,
            lesson=lesson
        )

        open_lessons.append({
            'lesson': lesson,
            'progress': progress,
            'is_open': True
        })

        if not progress.is_completed:
            break

    return open_lessons

def complete_lesson(user, lesson):
    if not user:
        return {
            'message': 'Пользователь не найден'
        }
    lesson_progres = get_object_or_404(LessonProgress, user = user, lesson=lesson)
    lesson_progres.is_completed = True
    lesson_progres.completed_at = now()
    lesson_progres.save(update_fields=['is_completed', 'completed_at'])
    print(f'Да вот прогрес {lesson_progres.is_completed}')
    # Заканчиваем урок если надо лол
    # Плюс открываем некст автоматом 