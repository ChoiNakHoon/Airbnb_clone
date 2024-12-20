from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


# 유저가 로그인 했을 때 보여지면 안 되는 페이지를 url로 접근 할려고 했을 때 의도 된 페이지로 이동 시킴

# Email유저 이외 유저가 접근 할 수 없는 페이지를 url로 접근 하려고 했을 때
class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


# 로그인 유저가 접근 할 수 없는 페이지를 url로 접근 하려고 했을때.
class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


# 로그 아웃인 상태인 유저가 접근 할 수 없는 페이지를 url로 접근 하려고 했을 때
class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
