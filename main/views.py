import base64
import datetime
import json
import os
import re
import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

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


# API for Flutter App
# =================================================================================================
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

            user = User.objects.get(username=username)
            # Successful login
            return JsonResponse(
                {
                    "id": str(user.id),
                    "username": user.username,
                    "role": user.role,
                    "phone_number": user.phone_number,
                    "address": user.address,
                    "profile_picture": (
                        user.profile_picture.url if user.profile_picture else None
                    ),
                    "status": True,
                    "message": "Login successful!",
                },
                status=200,
            )

        return JsonResponse(
            {"status": False, "message": "Login gagal, akun dinonaktifkan."},
            status=401,
        )

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

    try:
        data = json.loads(request.body)

        # Required fields validation
        required_fields = [
            "username",
            "password1",
            "password2",
            "phone_number",
            "address",
            "role",
        ]
        for field in required_fields:
            if not data.get(field):
                return JsonResponse(
                    {
                        "status": False,
                        "message": f"{field.replace('_', ' ').title()} is required",
                    },
                    status=400,
                )

        # Extract data
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")
        phone_number = data.get("phone_number")
        address = data.get("address")
        role = data.get("role")
        profile_picture = data.get("profile_picture")

        # Password validation
        if password1 != password2:
            return JsonResponse(
                {"status": False, "message": "Passwords do not match"},
                status=400,
            )

        # Username validation
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"status": False, "message": "Username is already in use"},
                status=400,
            )

        # Phone number validation (basic)
        if not re.match(r"^(\+62|62|0)8[1-9][0-9]{6,10}$", phone_number):
            return JsonResponse(
                {"status": False, "message": "Invalid phone number format"},
                status=400,
            )

        # Role validation
        role_map = {
            "Customer": User.CUSTOMER,
            "Restaurant Owner": User.RESTAURANT_OWNER,
        }

        if role not in role_map:
            return JsonResponse(
                {"status": False, "message": "Invalid role selected"},
                status=400,
            )

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password1,
            role=role_map[role],
            phone_number=phone_number,
            address=address,
        )

        # Handle profile picture
        if profile_picture:
            try:
                # Remove the "data:image/jpeg;base64," part if it exists
                if "," in profile_picture:
                    profile_picture = profile_picture.split(",")[1]

                # Decode the image
                image_data = base64.b64decode(profile_picture)

                # Generate a unique filename
                filename = f"{username}_profile_{uuid.uuid4()}.jpg"

                # Save the image to media directory
                path = default_storage.save(
                    os.path.join("profile_pics", filename), ContentFile(image_data)
                )

                # Update user with profile picture
                user.profile_picture = path
                user.save()
            except Exception as e:
                # Log the error, but don't prevent registration
                print(f"Error saving profile picture: {e}")

        return JsonResponse(
            {
                "id": str(user.id),
                "username": user.username,
                "role": role,
                "phone_number": user.phone_number,
                "status": "success",
                "message": "Registration successful!",
            },
            status=200,
        )

    except Exception as e:
        # Catch any unexpected errors
        return JsonResponse(
            {"status": False, "message": f"Registration failed: {str(e)}"},
            status=500,
        )


def mobile_get_user_data(request):
    if request.method != "GET":
        return JsonResponse(
            {"status": False, "message": "Method not allowed"}, status=405
        )

    user = request.user

    if user.is_authenticated:
        return JsonResponse(
            {
                "id": str(user.id),
                "username": user.username,
                "role": user.role,
                "phone_number": user.phone_number,
                "address": user.address,
                "profile_picture": (
                    user.profile_picture.url if user.profile_picture else None
                ),
                "status": "success",
            },
            status=200,
        )

    return JsonResponse(
        {"status": False, "message": "User is not authenticated"}, status=401
    )
