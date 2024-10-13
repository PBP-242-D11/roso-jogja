from django.urls import path

from main.views import register, show_main, user_login

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
]
