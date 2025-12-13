from django.urls import path
from .views import *

app_name = 'tests_app'

urlpatterns = [
    path('lesson_test/<int:lesson_id>/<int:question_order>/', lesson_test, name='lesson_test'),
    path('answer_question/<int:question_id>/', answer_question, name='answer_question'),
    path('answer_code/<int:question_id>/', answer_code, name='answer_code'),
    path('code_status/<int:code_attemp_id>/', code_status, name='code_status'),
    path('finish_test/<int:question_id>/', finish_test, name='finish_test')
]
