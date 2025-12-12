from datetime import datetime
from courses.models import Module, Lesson, Course
from .models import LessonProgress, ModuleProgress
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now




def get_all_open_modules(user, course: Course):
    if user.is_course_admin:
        return course.modules.all()
    modules = course.modules.order_by('order')
    open_moduls = []


    for module in modules:
        mod, _ = ModuleProgress.objects.get_or_create(user=user, module=module)

        if mod.is_unlocked or mod.module.order == 1:
            open_moduls.append(mod)
        else:
            break

    return open_moduls
    # Собираеся все открытие модули 



def get_all_open_lessons(user, module: Module):
    if user.is_course_admin:
        return module.lessons.all()
    lessons = module.lessons.order_by('order')
    open_lesson = []

    for lesson in lessons:
        les, _ = LessonProgress.objects.get_or_create(user=user, lesson=lesson)

        open_lesson.append(les)
        if not les.is_completed:
            break
    
    return open_lesson # СОбираем все открытые уроки 
    # крч логика такая собираем все уроки с нашего модуля и открываем один минимум 
    # ну крч добовляем всем задания которые у нас выполнены и +1 
    # что бы сильно с логикой не мучится так что как тока отметили is_completed на прошлом заданий то некст само откроется 

def complete_lesson(user, lesson):
    if not user:
        return {
            'message': 'Пользователь не найден'
        }
    lesson_progres = get_object_or_404(LessonProgress, user = user, lesson=lesson)
    lesson_progres.is_completed = True
    lesson_progres.completed_at = now()
    lesson_progres.save(update_fields=['is_completed', 'completed_at'])

    # Заканчиваем урок если надо лол
    # Плюс открываем некст автоматом 