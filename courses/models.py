from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)  # лучше TextField для длинного описания
    image = models.ImageField(upload_to='courses/course_img', verbose_name='Картинка курса')
    slug = models.SlugField(max_length=100, unique=True)  # используем SlugField и unique=True
    is_posted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)  # порядок отображения

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.name}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=True)  # текст урока
    video_url = models.URLField(blank=True, null=True)  # видео урок
    order = models.PositiveIntegerField(default=0)  # порядок урока в модуле
    has_test = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.name} - {self.title}"