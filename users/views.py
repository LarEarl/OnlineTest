from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

from .forms import RegisterForm, LoginForm, ProfileEditForm
from .services import authenticate_identifier_password
from .models import ActivationCode


class RegisterView(View):
	def get(self, request):
		form = RegisterForm()
		return render(request, 'users/register.html', {'form': form})

	def post(self, request):
		form = RegisterForm(request.POST)
		next_url = request.GET.get('next') or request.POST.get('next')
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False  # Деактивируем до верификации
			user.save()
			# Сигнал создаст ActivationCode и отправит письмо
			return redirect(reverse('users:verify'))
		return render(request, 'users/register.html', {'form': form})


class VerifyView(View):
	def get(self, request):
		email = request.GET.get('email', '')
		return render(request, 'users/verify.html', {'email': email})

	def post(self, request):
		email = request.POST.get('email')
		code = request.POST.get('code')

		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return render(request, 'users/verify.html', {
				'email': email,
				'error': 'Пользователь с таким email не найден'
			})

		activation = user.activation_codes.filter(used=False).first()
		if not activation:
			return render(request, 'users/verify.html', {
				'email': email,
				'error': 'Код верификации не найден или истек'
			})

		is_valid, error = activation.check_code(code)
		if is_valid:
			user.is_active = True
			user.save()
			login(request, user)
			return redirect(reverse('users:profile'))
		else:
			return render(request, 'users/verify.html', {
				'email': email,
				'error': error or 'Код неверный'
			})


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
				if not user.is_active:
					return render(request, 'users/login.html', {
						'form': form,
						'error': 'Аккаунт не активирован. Подтвердите email.'
					})
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


# Импорт User для VerifyView
from .models import User


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
