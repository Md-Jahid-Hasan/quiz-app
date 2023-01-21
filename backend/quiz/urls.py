from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GetQuizQuestion, SubmitQuestionView, GetQuizView

app_name = "quiz"

router = DefaultRouter()

urlpatterns = [
    path('quiz/', GetQuizView.as_view(), name="quiz"),
    path('attempt/<int:pk>/', GetQuizQuestion.as_view(), name="attempt"),
    path('submit/<int:pk>/', SubmitQuestionView.as_view(), name="submit")
]

