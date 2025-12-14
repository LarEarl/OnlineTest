import random
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
	email = models.EmailField()
	is_course_admin = models.BooleanField(default=False)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

	def __str__(self) -> str:
		return self.username


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
