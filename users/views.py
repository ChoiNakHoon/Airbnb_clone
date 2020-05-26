from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(View):
    def get(self, request):

        form = forms.LoginForm(initial={"user": "onehub86@likelion.org"})

        return render(request, "users/login.html", context={"form": form})

    def post(self, request):

        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            password = form.cleaned_data.get("password")
            login_user = authenticate(request, username=user, password=password)
            if login_user is not None:
                login(request, login_user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", context={"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
