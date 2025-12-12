from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from .views import (
    LoginView,
    RegisterView,
    LogoutView,
    ProfileView,
    ProfileEditView,
)

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('password-change/', PasswordChangeView.as_view(template_name='users/password_change.html', success_url='/users/profile/'), name='password_change'),
]
