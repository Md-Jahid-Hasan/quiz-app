import datetime
from django.http import Http404
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.views import APIView

from .serializers import QuestionSerializer, QuestionSerializerDetails, QuizSerializer, ChoiceQuestionSerializer, \
    UserQuizAnswerSerializer, UserQuizSerializer, ChoiceAnswerSerializer, QuizSerializerWithQuestion

from .models import Quiz, Question, UserQuiz, UserQuizAns, Choice


class GetQuizView(ListAPIView):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()


class GetQuizQuestion(RetrieveAPIView):
    serializer_class = QuizSerializerWithQuestion
    permission_classes = (IsAuthenticated,)
    queryset = Quiz.objects.all()

    def get_object(self):
        question_id = self.request.query_params.get('question', None)
        obj = super(GetQuizQuestion, self).get_object()
        questions = list(obj.questions.all())
        if question_id:
            try:
                obj = Question.objects.get(id=question_id, quiz_questions=obj)
            except Question.DoesNotExist:
                raise Http404
        else:
            user_quiz, created = UserQuiz.objects.get_or_create(user=self.request.user, quiz=obj)
            if created:
                q = (UserQuizAns(question=i, quiz=user_quiz) for i in questions)
                user_ans = UserQuizAns.objects.bulk_create(q)
        return obj

    def get_serializer_class(self):
        if self.request.query_params.get('question', None):
            return QuestionSerializer
        return self.serializer_class


class SubmitQuestionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        quiz_id = kwargs.get('pk')
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Invalid Quiz"}, status=HTTP_404_NOT_FOUND)

        try:
            user_quiz = UserQuiz.objects.get(user=self.request.user, quiz=quiz)
        except UserQuiz.DoesNotExist:
            return Response({"error": "You are not allowed to submit answer for this Quiz"}, status=HTTP_404_NOT_FOUND)

        questions = quiz.questions
        marks = 0

        for ans in request.data:
            try:
                question = questions.get(id=ans.get('question', None))
            except Question.DoesNotExist:
                return Response({"error": "There is a invalid question in your submission."}, status=HTTP_404_NOT_FOUND)
            try:
                choice = question.options.get(id=ans.get('ans', None))
                if choice.correct:
                    marks += 1
            except Choice.DoesNotExist:
                return Response({"error": "There is a invalid choice in your submission."}, status=HTTP_404_NOT_FOUND)

            user_ans = user_quiz.answer.get(question=question)
            user_ans.ans = choice
            user_ans.save()

        user_quiz.obtain_mark = marks
        user_quiz.submitted_at = datetime.datetime.now()
        user_quiz.save()

        user_ans_with_solution = UserQuizSerializer(user_quiz).data

        return Response(user_ans_with_solution, status=HTTP_200_OK)
