from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from .forms import RegisterForm, LoginForm, ProfileEditForm
from .services import authenticate_identifier_password
from .models import ActivationCode, User


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
			# Сохраняем ID юзера в сессию для верификации
			request.session['verify_user_id'] = user.id
			request.session['verify_email'] = user.email
			# Сигнал создаст ActivationCode и отправит письмо
			return redirect(reverse('users:verify'))
		return render(request, 'users/register.html', {'form': form})


class VerifyView(View):
	def get(self, request):
		email = request.session.get('verify_email', '')
		return render(request, 'users/verify.html', {'email': email})

	def post(self, request):
		code = request.POST.get('code')
		user_id = request.session.get('verify_user_id')
		
		if not user_id:
			return render(request, 'users/verify.html', {
				'error': 'Сессия истекла. Пожалуйста, зарегистрируйтесь заново'
			})
		
		try:
			user = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return render(request, 'users/verify.html', {
				'error': 'Пользователь не найден'
			})
		
		# Найти неиспользованный код для этого юзера
		activation = user.activation_codes.filter(used=False).first()
		
		if not activation:
			return render(request, 'users/verify.html', {
				'email': user.email,
				'error': 'Код верификации не найден или истек'
			})

		is_valid, error = activation.check_code(code)
		if is_valid:
			user.is_active = True
			user.save()
			# Очистить сессию
			request.session.pop('verify_user_id', None)
			request.session.pop('verify_email', None)
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			return redirect(reverse('users:profile'))
		else:
			return render(request, 'users/verify.html', {
				'email': user.email,
				'error': error or 'Код неверный'
			})


class ResendVerificationCodeView(View):
	def post(self, request):
		# Попытаемся получить юзера из сессии
		user_id = request.session.get('verify_user_id')
		
		if user_id:
			try:
				user = User.objects.get(id=user_id, is_active=False)
			except User.DoesNotExist:
				user = None
		else:
			# Если нет сессии, используем email из сессии
			email = request.session.get('verify_email')
			if email:
				user = User.objects.filter(email=email, is_active=False).order_by('-date_joined').first()
			else:
				user = None
		
		if not user:
			return render(request, 'users/verify.html', {
				'email': request.session.get('verify_email', ''),
				'error': 'Пользователь не найден'
			})
		
		# Удалить старые коды
		user.activation_codes.all().delete()
		
		# Создать новый код
		activation = ActivationCode.create_for_user(user)
		
		# Отправить email
		send_mail(
			'Код верификации',
			f'Ваш код верификации: {activation.raw_code}\nКод действителен 15 минут.',
			settings.DEFAULT_FROM_EMAIL,
			[user.email],
			fail_silently=False,
		)
		
		return render(request, 'users/verify.html', {
			'email': user.email,
			'success': 'Код верификации отправлен на вашу почту'
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
				login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
		form = ProfileEditForm(instance=request.user)
		return render(request, 'users/profile_edit.html', {'form': form})

	def post(self, request):
		form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
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
			user = form.save()
			# Если пароль был изменен, нужно обновить сессию
			if form.cleaned_data.get('new_password1'):
				from django.contrib.auth import update_session_auth_hash
				update_session_auth_hash(request, user)
			return redirect(reverse('users:profile'))
		return render(request, 'users/profile_edit.html', {'form': form})
