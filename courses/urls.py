from django.urls import path
from .views import *

app_name = 'courses'

urlpatterns = [
    path('all_cources/', all_cources , name='all_cources'),
    path('modules/<str:course_slug>/', modules, name='modules'),
    path('lessons/<str:modul_slug>/', lessons, name='lessons'),
    path('lesson/<int:lesson_id>/', lesson, name='lesson'),
]
