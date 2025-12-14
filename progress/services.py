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

        # Первый модуль в курсе всегда открыт
        is_first_module = module == modules.first()
        is_open = progress.is_unlocked or is_first_module

        open_modules.append({
            'module': module,
            'progress': progress,
            'is_open': is_open
        })

        # Останавливаемся после первого закрытого модуля
        if not is_open:
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
            'message': 'Пользователь не найден',
            'course_completed': False
        }
    
    lesson_progres = get_object_or_404(LessonProgress, user = user, lesson=lesson)
    lesson_progres.is_completed = True
    lesson_progres.completed_at = now()
    lesson_progres.save(update_fields=['is_completed', 'completed_at'])
    print(f'Урок завершен: {lesson_progres.is_completed}')
    
    course_completed = False
    completed_course_name = None
    
    # Проверяем, завершены ли все уроки в модуле
    module = lesson.module
    all_lessons = module.lessons.all()
    completed_lessons = LessonProgress.objects.filter(
        user=user,
        lesson__module=module,
        is_completed=True
    ).count()
    
    # Если все уроки модуля завершены, открываем следующий модуль
    if completed_lessons == all_lessons.count():
        print(f'Модуль {module.name} завершен полностью!')
        module_progress = ModuleProgress.objects.get(user=user, module=module)
        module_progress.is_unlocked = True
        module_progress.save()
        
        # Открываем следующий модуль
        next_module = Module.objects.filter(
            course=module.course,
            order=module.order + 1
        ).first()
        
        if next_module:
            next_module_progress, _ = ModuleProgress.objects.get_or_create(
                user=user,
                module=next_module
            )
            next_module_progress.is_unlocked = True
            next_module_progress.save()
            print(f'Следующий модуль {next_module.name} открыт!')
        else:
            # Это был последний модуль - проверяем, завершен ли весь курс
            course = module.course
            total_course_lessons = sum(m.lessons.count() for m in course.modules.all())
            completed_course_lessons = LessonProgress.objects.filter(
                user=user,
                lesson__module__course=course,
                is_completed=True
            ).count()
            
            if total_course_lessons == completed_course_lessons:
                course_completed = True
                completed_course_name = course.title
                completed_course_id = course.id
                print(f'КУРС "{course.title}" ПОЛНОСТЬЮ ЗАВЕРШЕН!')
                
                # Начисляем 100 XP за завершение курса
                old_level = user.level
                user.add_xp(100)
                new_level = user.level
                level_up = new_level > old_level
                
                return {
                    'success': True,
                    'course_completed': True,
                    'course_name': completed_course_name,
                    'course_id': completed_course_id,
                    'xp_gained': 100,
                    'level_up': level_up,
                    'new_level': new_level
                }
    
    return {
        'success': True,
        'course_completed': course_completed,
        'course_name': completed_course_name,
        'course_id': completed_course_id
    } 