from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, UserView, Welcome

app_name = 'accounts'

router = DefaultRouter()
router.register('user', UserView, basename="user")

urlpatterns = [
    path("", Welcome.as_view()),
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name="login"),
]