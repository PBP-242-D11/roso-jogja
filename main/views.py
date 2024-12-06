import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from main.forms import CustomRegisterForm


# Create your views here.
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
            return redirect("main:login")

    context = {"form": form}
    return render(request, "register.html", context)


def login_user(request):
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


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie("last_login")
    return redirect("main:login")


@login_required(login_url="/login/")
def get_user_data(request):
    profile_picture_url = None
    if request.user.profile_picture:
        profile_picture_url = request.user.profile_picture.url

    user_data = {
        "id": request.user.id,
        "role": request.user.role,
        "username": request.user.username,
        "phone_number": request.user.phone_number,
        "address": request.user.address,
        "profile_picture": profile_picture_url,
    }

    return JsonResponse(user_data)


import json

from django.contrib.auth import authenticate, get_user_model

# API for Flutter App
# =================================================================================================
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


@csrf_exempt
def mobile_login(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": False, "message": "Method not allowed"}, status=405
        )

    # Get username and password from request
    username = request.POST.get("username")
    password = request.POST.get("password")

    # Check if username and password are provided
    if not username or not password:
        return JsonResponse(
            {"status": False, "message": "Username and password are required"},
            status=400,
        )

    # Authenticate user
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            # Successful login
            return JsonResponse(
                {
                    "username": user.username,
                    "email": user.email,  # Add email if you want
                    "status": True,
                    "message": "Login sukses!",
                    # You can add more user fields from your custom model here
                },
                status=200,
            )
        else:
            return JsonResponse(
                {"status": False, "message": "Login gagal, akun dinonaktifkan."},
                status=401,
            )
    else:
        return JsonResponse(
            {
                "status": False,
                "message": "Login gagal, periksa kembali email atau kata sandi.",
            },
            status=401,
        )


@csrf_exempt
def mobile_register(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": False, "message": "Method not allowed"}, status=405
        )

    data = json.loads(request.body)
    username = data.get("username")
    password1 = data.get("password1")
    password2 = data.get("password2")

    if not username or not password1 or not password2:
        return JsonResponse(
            {"status": False, "message": "Username and password are required"},
            status=400,
        )

    if password1 != password2:
        return JsonResponse(
            {"status": False, "message": "Password tidak sama"},
            status=400,
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"status": False, "message": "Username sudah digunakan"},
            status=400,
        )

    user = User.objects.create_user(username=username, password=password1)
    user.save()

    return JsonResponse(
        {
            "username": user.username,
            "email": user.email,  # Add email if you want
            "status": "success",
            "message": "Register sukses!",
            # You can add more user fields from your custom model here
        },
        status=200,
    )
