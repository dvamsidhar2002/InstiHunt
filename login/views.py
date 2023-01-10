from django.shortcuts import redirect, render
from .forms import SignupForm, UserCreationForm, loginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate


# Create your views here.
def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home_page")
        else:
            return redirect("login_page")
    context = {}
    return render(request, "login/login.html", context)


def signup_page(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            form.save()
            new_user = authenticate(username=username, password=password)
            new_user.save()
            if new_user is not None:
                login(request, new_user)
                return redirect("home_page")
    else:
        form = SignupForm()
    context = {"form": form}
    return render(request, "login/signup.html", context)


def logout_page(request):
    logout(request)
    return redirect("home_page")
