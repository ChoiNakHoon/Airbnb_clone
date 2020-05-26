from django import forms
from . import models


class LoginForm(forms.Form):

    user = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        user = self.cleaned_data.get("user")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=user)
            if user.check_password(password):
                return password
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("user", forms.ValidationError("User does not exist"))
