import random
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
	email = models.EmailField()
	is_course_admin = models.BooleanField(default=False)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
	level = models.IntegerField(default=0)
	xp = models.IntegerField(default=0)

	def __str__(self) -> str:
		return self.username
	
	def get_xp_for_next_level(self):
		"""Возвращает необходимое количество XP для следующего уровня (последовательность Фибоначчи)"""
		if self.level == 0:
			return 100
		elif self.level == 1:
			return 200
		elif self.level == 2:
			return 300
		else:
			# Для уровней 3+ используем последовательность Фибоначчи: 500, 800, 1300, 2100...
			fib_prev_prev = 300
			fib_prev = 500
			for i in range(3, self.level + 1):
				fib_current = fib_prev_prev + fib_prev
				fib_prev_prev = fib_prev
				fib_prev = fib_current
			return fib_prev
	
	def add_xp(self, amount):
		"""Добавляет XP и автоматически повышает уровень при достижении порога"""
		self.xp += amount
		
		while True:
			xp_needed = self.get_xp_for_next_level()
			if self.xp >= xp_needed:
				self.xp -= xp_needed
				self.level += 1
			else:
				break
		
		self.save()
		return self.level
	
	def get_xp_progress_percent(self):
		"""Возвращает прогресс в процентах до следующего уровня"""
		xp_needed = self.get_xp_for_next_level()
		if xp_needed == 0:
			return 100
		return int((self.xp / xp_needed) * 100)


class ActivationCode(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_codes')
	code = models.CharField(max_length=4)
	created_at = models.DateTimeField(auto_now_add=True)
	expires_at = models.DateTimeField()
	used = models.BooleanField(default=False)
	attempts = models.IntegerField(default=0)

	@staticmethod
	def random_code():
		raw_code = ''
		for i in range(4):
			raw_code += str(random.randint(0, 9))
		return raw_code

	@classmethod
	def create_for_user(cls, user, lifetime_minutes=15):
		raw_code = cls.random_code()
		obj = cls.objects.create(
			user=user,
			code=raw_code,
			expires_at=timezone.now() + timedelta(minutes=lifetime_minutes)
		)
		return obj, raw_code
	
	def is_valid(self):
		return (not self.used) and (timezone.now() < self.expires_at)
	
	def check_code(self, code, max_attempts=3):
		if self.used:
			return False, 'Код уже использован'
		if timezone.now() > self.expires_at:
			return False, 'Код истек'
		if self.attempts >= max_attempts:
			return False, 'Превышено количество попыток'
		if self.code == code:
			self.used = True
			self.save()
			return True, None
		self.attempts += 1
		self.save()
		return False, 'Неверный код'

	def __str__(self):
		return f"{self.user.username} - {self.code}"
