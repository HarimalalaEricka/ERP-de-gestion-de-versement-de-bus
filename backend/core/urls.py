from django.urls import path
from core.controllers.auth_controller import login, register

urlpatterns = [
    path("auth/login/", login, name="login"),
    path("auth/register/", register, name="register"),
]