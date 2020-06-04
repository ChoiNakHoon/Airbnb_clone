from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin


# 유저가 로그인 했을 때 보여지면 안 되는 페이지를 url로 접근 할려고 했을 때
# 메인 페이지로 이동
class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authentucated

    def handle_no_permission(self):
        return redirect("core:home")
