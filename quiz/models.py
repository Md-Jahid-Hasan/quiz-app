from django.db import models
from django.contrib.auth import get_user_model as User


class Quiz(models.Model):
    created_by = models.ForeignKey(User(), related_name="quiz_creator", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField('Question', related_name="quiz_questions")
    attempted_user = models.ManyToManyField(User(), related_name="user_quiz", through="UserQuiz")


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=255)
    marks = models.DecimalField(default=1, decimal_places=1, max_digits=3)
    # option1 = models.ForeignKey('Choice', related_name="option1", on_delete=models.SET_NULL, null=True, blank=True)
    # option2 = models.ForeignKey('Choice', related_name="option2", on_delete=models.SET_NULL, null=True, blank=True)
    # option3 = models.ForeignKey('Choice', related_name="option3", on_delete=models.SET_NULL, null=True, blank=True)
    # option4 = models.ForeignKey('Choice', related_name="option4", on_delete=models.SET_NULL, null=True, blank=True)
    help_text = models.CharField(max_length=100, null=True, blank=True)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    correct = models.BooleanField()


class UserQuiz(models.Model):
    user = models.ForeignKey(User(), on_delete=models.CASCADE, related_name='attempted_user')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempted_quiz')
    submitted_at = models.DateTimeField(null=True, blank=True)
    obtain_mark = models.DecimalField(decimal_places=1, null=True, blank=True, max_digits=3)


class UserQuizAns(models.Model):
    quiz = models.ForeignKey(UserQuiz, on_delete=models.CASCADE, related_name="answer")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="user_question_ans")
    ans = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True)
