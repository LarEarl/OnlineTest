from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from courses.models import Course, Module, Lesson
from tests_app.models import Test, Question, AnswerOption
from users.models import User
from progress.models import LessonProgress

from .forms import CourseForm, ModuleForm, LessonForm, TestForm, QuestionForm, AnswerOptionForm


def teacher_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_course_admin, login_url='users:login')(view_func))


@teacher_required
def dashboard(request):
    courses_count = Course.objects.count()
    modules_count = Module.objects.count()
    lessons_count = Lesson.objects.count()
    tests_count = Test.objects.count()

    students_count = User.objects.filter(is_course_admin=False).count()

    return render(request, 'teacher_app/dashboard.html', {
        'courses_count': courses_count,
        'modules_count': modules_count,
        'lessons_count': lessons_count,
        'tests_count': tests_count,
        'students_count': students_count,
    })


@teacher_required
def courses_manage(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс создан')
            return redirect('teacher_app:courses')
        messages.error(request, 'Исправьте ошибки формы')
    else:
        form = CourseForm()

    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'teacher_app/courses.html', {'form': form, 'courses': courses})


@teacher_required
def modules_manage(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Модуль создан')
            return redirect('teacher_app:modules')
        messages.error(request, 'Исправьте ошибки формы')
    else:
        form = ModuleForm()

    modules = Module.objects.select_related('course').order_by('course__title', 'order')
    return render(request, 'teacher_app/modules.html', {'form': form, 'modules': modules})


@teacher_required
def lessons_manage(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Урок создан')
            return redirect('teacher_app:lessons')
        messages.error(request, 'Исправьте ошибки формы')
    else:
        form = LessonForm()

    lessons = Lesson.objects.select_related('module', 'module__course').order_by('module__course__title', 'module__order', 'order')
    return render(request, 'teacher_app/lessons.html', {'form': form, 'lessons': lessons})


@teacher_required
def tests_manage(request):
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        question_form = QuestionForm(request.POST)
        answer_form = AnswerOptionForm(request.POST)

        if test_form.is_valid():
            test = test_form.save()
            messages.success(request, 'Тест создан')
            return redirect('teacher_app:tests')
        elif question_form.is_valid():
            question = question_form.save()
            messages.success(request, 'Вопрос добавлен')
            return redirect('teacher_app:tests')
        elif answer_form.is_valid():
            answer_form.save()
            messages.success(request, 'Ответ добавлен')
            return redirect('teacher_app:tests')
        else:
            messages.error(request, 'Исправьте ошибки формы')
    else:
        test_form = TestForm()
        question_form = QuestionForm()
        answer_form = AnswerOptionForm()

    tests = Test.objects.select_related('lesson', 'lesson__module', 'lesson__module__course').order_by('-id')
    questions = Question.objects.select_related('test').order_by('test__title', 'order')

    return render(request, 'teacher_app/tests.html', {
        'test_form': test_form,
        'question_form': question_form,
        'answer_form': answer_form,
        'tests': tests,
        'questions': questions,
    })


@teacher_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс обновлен')
            return redirect('teacher_app:courses')
        messages.error(request, 'Исправьте ошибки формы')
    else:
        form = CourseForm(instance=course)

    return render(request, 'teacher_app/course_edit.html', {'form': form, 'course': course})


@teacher_required
def module_edit(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, 'Модуль обновлен')
            return redirect('teacher_app:modules')
        messages.error(request, 'Исправьте ошибки формы')
    else:
        form = ModuleForm(instance=module)

    return render(request, 'teacher_app/module_edit.html', {'form': form, 'module': module})


@teacher_required
def lesson_edit(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'Урок обновлен')
            return redirect('teacher_app:lessons')
        messages.error(request, 'Исправьте ошибки формы')
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'teacher_app/lesson_edit.html', {'form': form, 'lesson': lesson})


@teacher_required
def test_edit(request, pk):
    test = get_object_or_404(Test, pk=pk)
    
    # Обработка редактирования вопросов
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'edit_test':
            form = TestForm(request.POST, instance=test)
            if form.is_valid():
                form.save()
                messages.success(request, 'Тест обновлен')
                return redirect('teacher_app:test_edit', pk=pk)
            messages.error(request, 'Исправьте ошибки формы')
        
        elif action == 'edit_question':
            question_id = request.POST.get('question_id')
            question = get_object_or_404(Question, id=question_id, test=test)
            question.text = request.POST.get('text')
            question.order = request.POST.get('order')
            question.save()
            messages.success(request, 'Вопрос обновлен')
            return redirect('teacher_app:test_edit', pk=pk)
        
        elif action == 'delete_question':
            question_id = request.POST.get('question_id')
            question = get_object_or_404(Question, id=question_id, test=test)
            question.delete()
            messages.success(request, 'Вопрос удален')
            return redirect('teacher_app:test_edit', pk=pk)
        
        elif action == 'edit_option':
            option_id = request.POST.get('option_id')
            option = get_object_or_404(AnswerOption, id=option_id)
            option.text = request.POST.get('text')
            option.is_correct = request.POST.get('is_correct') == 'on'
            option.save()
            messages.success(request, 'Ответ обновлен')
            return redirect('teacher_app:test_edit', pk=pk)
        
        elif action == 'delete_option':
            option_id = request.POST.get('option_id')
            option = get_object_or_404(AnswerOption, id=option_id)
            option.delete()
            messages.success(request, 'Ответ удален')
            return redirect('teacher_app:test_edit', pk=pk)
    
    form = TestForm(instance=test)
    questions = test.questions.prefetch_related('options').order_by('order')
    
    return render(request, 'teacher_app/test_edit.html', {
        'form': form,
        'test': test,
        'questions': questions
    })


@teacher_required
def students(request):
    students_qs = User.objects.filter(is_course_admin=False).order_by('-date_joined')

    student_stats = []
    for student in students_qs:
        completed_lessons = LessonProgress.objects.filter(user=student, is_completed=True).count()
        total_lessons = Lesson.objects.count()
        progress_percent = int((completed_lessons / total_lessons) * 100) if total_lessons else 0

        student_stats.append({
            'user': student,
            'completed_lessons': completed_lessons,
            'total_lessons': total_lessons,
            'progress_percent': progress_percent,
            'level': student.level,
            'xp': student.xp,
        })

    return render(request, 'teacher_app/students.html', {'student_stats': student_stats})


@teacher_required
def question_move(request, pk, direction):
    question = get_object_or_404(Question, pk=pk)
    test = question.test
    questions = list(test.questions.order_by('order'))
    
    current_index = questions.index(question)
    
    if direction == 'up' and current_index > 0:
        # Меняем местами с предыдущим
        prev_question = questions[current_index - 1]
        question.order, prev_question.order = prev_question.order, question.order
        question.save()
        prev_question.save()
        messages.success(request, 'Вопрос перемещен вверх')
    
    elif direction == 'down' and current_index < len(questions) - 1:
        # Меняем местами со следующим
        next_question = questions[current_index + 1]
        question.order, next_question.order = next_question.order, question.order
        question.save()
        next_question.save()
        messages.success(request, 'Вопрос перемещен вниз')
    
    return redirect('teacher_app:test_edit', pk=test.pk)
