from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from courses.models import Lesson, Module
from progress.models import LessonProgress, ModuleProgress
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

@receiver(post_save, LessonProgress)
def module_unlock_check(sender, instance, created,**kwargs):
    user = instance.user
    module = instance.lesson.module
    total_lesson = module.lessons.count()
    module_progress, _ = ModuleProgress.objects.get_or_create(user=user, module=module)

    completed_count = LessonProgress.objects.filter(
        user=user,
        lesson__module = module,
        is_completed = True
    ).count()

    if instance.is_completed:
        module_progress.completed_lessons_count = completed_count

    if module_progress.completed_lessons_count == total_lesson:
        module_progress.completed_at = now()
        module_progress.save(update_fields=['completed_lessons_count', 'completed_at'])

        next_module = Module.objects.filter(
            course = module.course,
            order = module.order + 1
            ).first()

        if next_module:
            
            next_module_progress, _ = ModuleProgress.objects.get_or_create(
                user = user,
                module = next_module
            )
            
            next_module_progress.is_unlocked = True
            next_module_progress.save(update_fields=['is_unlocked'])
            print('signal сработал и все гуд')
        