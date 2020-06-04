import os
import requests
from django.views.generic import FormView, DetailView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
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
    messages.warning(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

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
                raise GithubException("Can't get authorization code.")
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
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        # user가 데이터베이스 없다면 생성
                        user = models.User.objects.create(
                            username=email,
                            email=email,
                            first_name=name,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        # 소셜로그인 경우 꼭 필요함.
                        user.set_unusable_password()
                        user.save()
                    messages.success(request, f"Welcome back {user.first_name}")
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    # None면 제대로 가져 온게 아니기 때문에 GitHubException 호출
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get access code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"

    # 카카오 로그인 get url 넘기기
    # scope = 원하는 정보, email 뭐 이런거 사용자 동의가 있어야 가능한데 만약 동의 화면이 나타나지 않으면 여기서 지정해줘야 함..
    # 이것때문에 f..
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=account_email,profile"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        api_request = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = api_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        params = 'property_keys=["kakao_account.email"]'
        user_request = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
            data=params,
        )
        profile_json = user_request.json()
        email = profile_json.get("kakao_account").get("email", None)

        if email is None:
            raise KakaoException("Please also give me your email")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            # 여기서 현재 user_db에 존재하는지 판단
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                # 로그인 시도 하는데 Kakao가 아니면
                raise KakaoException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=email,
                email=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            # 소셜로그인 비밀번호 필요 없음
            user.set_unusable_password
            user.save()
            if profile_image is not None:
                # 이미지가 있으면
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar.jpg", ContentFile(photo_request.content),
                )
        messages.success(request, f"Welcome back {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        raise KakaoException()


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"
