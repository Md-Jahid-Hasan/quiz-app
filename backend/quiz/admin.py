from django.contrib import admin
from .models import Quiz, Question, UserQuiz, UserQuizAns, Choice

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(UserQuiz)
admin.site.register(UserQuizAns)
admin.site.register(Choice)
