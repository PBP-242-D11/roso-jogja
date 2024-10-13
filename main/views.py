import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from main.forms import CustomRegisterForm


# Create your views here.
@login_required(login_url="/login/")
def show_main(request):
    context = {
        "user": request.user,
        "last_login": request.COOKIES.get("last_login"),
    }

    return render(request, "main.html", context)


def register(request):
    form = CustomRegisterForm()

    if request.method == "POST":
        form = CustomRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("main:register")

    context = {"form": form}
    return render(request, "register.html", context)


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie(
                "last_login",
                str(datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p")),
            )
            return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    else:
        form = AuthenticationForm(request)
    context = {"form": form}
    return render(request, "login.html", context)
