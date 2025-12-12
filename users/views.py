from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

from .forms import RegisterForm, LoginForm, ProfileEditForm
from .services import authenticate_identifier_password


class RegisterView(View):
	def get(self, request):
		form = RegisterForm()
		return render(request, 'users/register.html', {'form': form})

	def post(self, request):
		form = RegisterForm(request.POST)
		next_url = request.GET.get('next') or request.POST.get('next')
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect(next_url or reverse('users:profile'))
		return render(request, 'users/register.html', {'form': form})


class LoginView(View):
	def get(self, request):
		form = LoginForm()
		return render(request, 'users/login.html', {'form': form})

	def post(self, request):
		form = LoginForm(request.POST)
		next_url = request.GET.get('next') or request.POST.get('next')
		if form.is_valid():
			identifier = form.cleaned_data['identifier']
			password = form.cleaned_data['password']
			user = authenticate_identifier_password(identifier, password)
			if user:
				login(request, user)
				if not form.cleaned_data.get('remember_me'):
					request.session.set_expiry(0)
				return redirect(next_url or reverse('users:profile'))
			else:
				form.add_error(None, 'Неверные данные для входа.')
		return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
	def get(self, request):
		# Страница подтверждения
		return render(request, 'users/logout_confirm.html')

	def post(self, request):
		logout(request)
		next_url = request.GET.get('next') or request.POST.get('next')
		return redirect(next_url or reverse('users:login'))


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		return render(request, 'users/profile.html', {'user_obj': request.user})


@method_decorator(login_required, name='dispatch')
class ProfileEditView(View):
	def get(self, request):
		form = ProfileEditForm(instance=request.user, user=request.user)
		return render(request, 'users/profile_edit.html', {'form': form})

	def post(self, request):
		form = ProfileEditForm(request.POST, request.FILES, instance=request.user, user=request.user)
		if form.is_valid():
			form.save()
			return redirect(reverse('users:profile'))
		return render(request, 'users/profile_edit.html', {'form': form})
