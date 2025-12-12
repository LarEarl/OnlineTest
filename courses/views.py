from django.shortcuts import render
from .models import Course, Module, Lesson
from progress.services import get_all_open_modules, get_all_open_lessons
from django.contrib.auth.decorators import login_required
# Create your views here.



def all_cources(request):
    cources = Course.objects.all()
    return render(request,'all_cources.html', { 'cources': cources })

@login_required()
def modules(request, course_slug):
    user = request.user
    course = Course.objects.get(slug=course_slug)
    open_moduls = get_all_open_modules(user, course) # получаем все открытые модули 

    return render(request, 'modules.html', { 'open_moduls': open_moduls })

@login_required()
def lessons(request, modul_slug):
    user = request.user
    module = Module.objects.get(slug=modul_slug)
    open_lessons = get_all_open_lessons(user, module) # получаем все открытые уроки по модулю
    

    return render(request, 'lessons.html', { 'open_lessons': open_lessons })

@login_required()
def lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    # получаем урок лол

    return render(request, 'lesson.html', { 'lesson': lesson })
