from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main.views import register, user_login

app_name = "main"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
