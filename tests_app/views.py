import json
from django.shortcuts import render
from courses.models import Lesson
from tests_app.models import *
from django.http import JsonResponse
from .tasks import run_code_task
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from progress.services  import complete_lesson
# Create your views here.
def lesson_test(request, lesson_id, question_order):
    lesson = Lesson.objects.get(id=lesson_id)
    test = lesson.tests.first()
    question = Question.objects.get(
        test=test,
        order=question_order
    )
    # отдаём страничку с вопросо заранее получив вопрос по lesson_id и question_order - это типа порядок вопроса
    return render(request,'lesson_test.html', { 'question': question })


def answer_code(request, question_id): # ednpoint для js AJAX если тип вопроса code (Создат очередь для выполнения задачи)
    if request.method == 'POST':
        question = Question.objects.get(id=question_id)

        if not question.is_code:
            return JsonResponse({'message': 'Not a code question'}, status=400)

        code = request.POST.get('code')

        # Используем create() чтобы пользователь мог отправлять код много раз
        code_attemp = CodeAttempt.objects.create(
            user = request.user,
            question = question,
            code = code,
        )

        run_code_task.delay(code_attempt_id=code_attemp.id)
        
        return JsonResponse(
            {
                'message': 'Код успешно отправился на проверку',
                'status': code_attemp.status,
                'attempt_id': code_attemp.id
            }
        )
        


def answer_question(request, question_id): # ednpoint для js AJAX если тип вопроса quiz
    if request.method == 'POST':
        question = Question.objects.get(id=question_id)
        
        user_selected = request.POST.get('user_answer')
        user_selected_option = AnswerOption.objects.get(id=user_selected)

        user_attempt, created = AnswerAttempt.objects.get_or_create(
            user=request.user,
            question=question,
        )
        
        # Добавляем выбранный вариант
        user_attempt.selected_options.add(user_selected_option)
        
        # Проверяем правильность ответа
        is_correct = user_selected_option.is_correct
        user_attempt.is_correct = is_correct
        user_attempt.save()
        print(user_attempt.is_correct)

        if is_correct:
            return JsonResponse(
                {
                    'message': 'Верный ответ!',
                    'answer': True
                }
            )
        else:
            return JsonResponse(
                {
                    'message': 'Ответ не верный',
                    'answer': False
                }
            )



def code_status(request, code_attemp_id): # ПРоверка статуса поптыка для пайтон кода поссылать запросы на этот endpoint на js
    code_attemp = get_object_or_404(CodeAttempt, id=code_attemp_id)
    
    return JsonResponse(
        {
            'status': code_attemp.status,
            'is_correct': code_attemp.is_correct,
            'stdout': code_attemp.stdout,
            'stderr': code_attemp.stderr,
        }
    )



@login_required
def finish_test(request, question_id):
    if request.method == 'POST':
        question = Question.objects.get(id=question_id)
        test = question.test
        user = request.user
        
        # Получаем все вопросы теста
        all_questions = test.questions.all()
        
        all_correct = True
        answered_count = 0
        
        for q in all_questions:
            if q.is_code:
                # Для code вопросов берем последнюю успешную попытку
                code_attempts = CodeAttempt.objects.filter(
                    user=user,
                    question=q,
                    status='success'
                ).order_by('-created_at')
                
                if code_attempts.exists() and code_attempts.first().is_correct:
                    answered_count += 1
                else:
                    all_correct = False
            else:
                # Для quiz вопросов
                quiz_attempt = AnswerAttempt.objects.filter(
                    user=user,
                    question=q
                ).first()
                
                if quiz_attempt and quiz_attempt.is_correct:
                    answered_count += 1
                else:
                    all_correct = False
        
        # Проверяем что все вопросы отвечены и правильны
        if all_correct and answered_count == all_questions.count():
            complete_lesson(user, lesson=test.lesson)
            return JsonResponse(
                {
                    'message': f'Поздравляем! Тест пройден ({answered_count}/{all_questions.count()})!',
                    'status': 'success'
                }
            )
        else:
            return JsonResponse(
                {
                    'message': f'Тест не пройден. Правильных ответов: {answered_count}/{all_questions.count()}',
                    'status': 'failed'
                }
            )