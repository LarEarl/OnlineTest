from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	email = models.EmailField(unique=True)
	is_course_admin = models.BooleanField(default=False)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

	def __str__(self) -> str:
		return self.username
