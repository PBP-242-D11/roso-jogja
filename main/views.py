from django.contrib import messages
from django.shortcuts import redirect, render

from main.forms import CustomRegisterForm


# Create your views here.
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
