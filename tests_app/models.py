# tests_app/models.py
from django.db import models
from courses.models import Lesson
from users.models import User


class Test(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tests")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    



    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    is_code = models.BooleanField(default=False)  # True если Python задача
    order = models.PositiveIntegerField(default=0)  # порядок вопросов в тесте

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.test.title} - {self.text[:50]}"


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"





class AnswerAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(AnswerOption, blank=True)
    text_answer = models.TextField(blank=True)

    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AnswerAttempt: {self.user} - {self.question.id}"


class CodeAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField()

    status = models.CharField(
        max_length=15,
        choices=(
            ("pending", "Pending"),
            ("running", "Running"),
            ("success", "Success"),
            ("failed", "Failed"),
        ),
        default="pending"
    )

    is_correct = models.BooleanField(null=True)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"CodeAttempt: {self.user} - {self.question.id} ({self.status})"


class CodeTestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="code_cases")
    input_data = models.TextField(blank=True)
    expected_output = models.TextField()
    time_limit = models.FloatField(default=1.0)  # seconds

    def __str__(self):
        return f"CodeTestCase for {self.question.id}"