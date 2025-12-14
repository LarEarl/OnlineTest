from django.urls import path
from . import views

app_name = 'teacher_app'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('courses/', views.courses_manage, name='courses'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('modules/', views.modules_manage, name='modules'),
    path('modules/<int:pk>/edit/', views.module_edit, name='module_edit'),
    path('lessons/', views.lessons_manage, name='lessons'),
    path('lessons/<int:pk>/edit/', views.lesson_edit, name='lesson_edit'),
    path('tests/', views.tests_manage, name='tests'),
    path('tests/<int:pk>/edit/', views.test_edit, name='test_edit'),
    path('questions/<int:pk>/move/<str:direction>/', views.question_move, name='question_move'),
    path('students/', views.students, name='students'),
]
