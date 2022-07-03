from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model as User

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = (AllowAny,)


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User().objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        return super(UserView, self).get_permissions()


class Welcome(APIView):
    def get(self, request, **kwargs):
        details = {
            'login': request.build_absolute_uri(reverse('accounts:login')),
            'create_user': request.build_absolute_uri(reverse('accounts:user-list')),
            'get_all_quiz_question': request.build_absolute_uri(reverse('quiz:attempt', kwargs={'pk': 1})),
            'get_specific_quiz_question': request.build_absolute_uri(
                reverse('quiz:attempt', kwargs={'pk': 1})) + "?question=1",
            'submit_quiz_answer': request.build_absolute_uri(reverse('quiz:submit', kwargs={'pk': 1})),

        }
        return Response(details, status=HTTP_200_OK)
