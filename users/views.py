import os
import requests
from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from . import forms
from . import models


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
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
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    print(f"이것은 인증 키 : {key}")
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do : add success msg
    except models.User.DoesNotExist:
        # to do : add error msg
        pass
    return redirect(reverse("core:home"))


def github_login(self):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize/?client_id={client_id}&redirect_url={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        # GitHub에서 로그인 인증 된 이후 설정된 리다이렉트 url로 code 전송
        code = request.GET.get("code", None)
        # GH_ID, GH_SECRET
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")

        if code is not None:
            # requests api를 이용해서 post
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            result_json = result.json()
            json_error = result_json.get("error", None)
            if json_error is not None:
                # 에러 나면 GithubException 호출
                raise GithubException()
            else:
                # 에러가 나지 않으면 access_token을 가져 온 다음
                access_token = result_json.get("access_token", None)
                # user_api를 호출한다. headers에 access_token을 넣는다.
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                # 응답 받은 json array를 저장 한 다음
                profile_json = profile_request.json()
                # login data를 가져 온다.
                username = profile_json.get("login", None)
                if username is not None:
                    # None 아니면 제대로 user_api json을 가져 온 것이니깐 원하는 data를 가져 온다.
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        # 여기서 현재 user_db에 존재하는지 판단
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            # 로그인 시도 했을 때 GitHub가 아니라면
                            raise GithubException()
                    except models.User.DoesNotExist:
                        # user가 데이터베이스 없다면 생성
                        user = models.User.objects.create(
                            username=email,
                            email=email,
                            first_name=name,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        # 소셜로그인 경우 꼭 필요함.
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    # None면 제대로 가져 온게 아니기 때문에 GitHubException 호출
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        return redirect(reverse("users:login"))


def kakao_login(self):
    pass
