from django.urls import path

from main.views import (
    get_user_data,
    login_user,
    logout_user,
    mobile_login,
    mobile_logout,
    mobile_register,
    register,
    show_main,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("user/", get_user_data, name="get_user_data"),
    path("mobile_login/", mobile_login, name="mobile_login"),
    path("mobile_register/", mobile_register, name="mobile_register"),
    path("mobile_logout/", mobile_logout, name="mobile_logout"),
]
