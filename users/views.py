from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    def get(self, request):

        form = forms.LoginForm(initial={"user": "onehub86@likelion.org"})

        return render(request, "users/login.html", context={"form": form})

    def post(self, request):

        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        return render(request, "users/login.html", context={"form": form})
