from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main.views import register

app_name = "main"

urlpatterns = [
    path("register/", register, name="register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
