from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('my/', views.my_progress, name='my_progress'),
    path('complete/<int:lesson_id>/', views.complete_lesson_view, name='complete_lesson'),
]
