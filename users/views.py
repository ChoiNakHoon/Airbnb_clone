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

    # def post(self, request):

    #     form = forms.LoginForm(request.POST)
    #     if form.is_valid():
    #         user = form.cleaned_data.get("user")
    #         password = form.cleaned_data.get("password")
    #         login_user = authenticate(request, username=user, password=password)
    #         if login_user is not None:
    #             login(request, login_user)
    #             return redirect(reverse("core:home"))
    #     return render(request, "users/login.html", context={"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
