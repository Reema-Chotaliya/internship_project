# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignupForm, UserLoginForm

def home(request):
    return render(request, "core/index.html")

def userSignupView(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserSignupForm()
    return render(request, "core/signup.html", {"form": form})

def userLoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                if user.role == "owner":
                    return redirect("localcommunity:business_owner")
                return redirect("home")
    else:
        form = UserLoginForm()
    return render(request, "core/login.html", {"form": form})

def custom_logout(request):
    logout(request)
    return redirect("home")