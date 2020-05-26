from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        user = form.cleaned_data.get("user")
        password = form.cleaned_data.get("password")
        login_user = authenticate(self.request, username=user, password=password)
        if login_user is not None:
            login(self.request, login_user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "firstname": "Raccoon",
        "lastname": "86",
        "email": "onehub86@likelion.org",
    }

    def form_valid(self, form):
        form.save()
        user = form.cleaned_data.get("user")
        password = form.cleaned_data.get("password")
        login_user = authenticate(self.request, username=user, password=password)
        if login_user is not None:
            login(self.request, login_user)
        return super().form_valid(form)
