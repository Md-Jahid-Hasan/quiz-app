from rest_framework import serializers
from .models import Quiz, Question, UserQuiz, UserQuizAns, Choice


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ("created_at", "name", )

class ChoiceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('text', )


class QuestionSerializer(serializers.ModelSerializer):
    options = ChoiceQuestionSerializer(many=True)

    class Meta:
        model = Question
        exclude = ('created_at', )


class QuizSerializerWithQuestion(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ("created_at", "questions", )


class ChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        exclude = ('question', )


class QuestionSerializerDetails(QuestionSerializer):
    options = ChoiceAnswerSerializer(many=True)
    # option2 = ChoiceAnswerSerializer()
    # option3 = ChoiceAnswerSerializer()
    # option4 = ChoiceAnswerSerializer()


class UserQuizAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializerDetails()
    ans = ChoiceAnswerSerializer()

    class Meta:
        model = UserQuizAns
        fields = ('question', 'ans', )


class UserQuizSerializer(serializers.ModelSerializer):
    answer = UserQuizAnswerSerializer(many=True)

    class Meta:
        model = UserQuiz
        fields = ('obtain_mark', 'submitted_at', 'answer')


