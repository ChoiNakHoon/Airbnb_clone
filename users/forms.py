from django import forms
from . import models


class LoginForm(forms.Form):

    user = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        user = self.cleaned_data.get("user")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=user)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
            return user
        except models.User.DoesNotExist:
            self.add_error("user", forms.ValidationError("User does not exist"))


class SignUpForm(forms.Form):
    firstname = forms.CharField(max_length=80)
    lastname = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이미 이메일이 사용 중입니다.")
        except models.User.DoesNotExist:
            return email

    # cleaned_apssword1만 받아오는 건 흐름 상 password가 먼저 받기 때문에 동시에 비교가 안 되서?
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        print(f"password : {password}")
        print(f"password1 : {password1}")
        if password != password1:
            raise forms.ValidationError("입력하신 비밀번호가 맞지 않습니다!")
        return password

    def save(self):
        firstname = self.cleaned_data.get("firstname")
        lastname = self.cleaned_data.get("lastname")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(email, email=email, password=password)
        user.firstname = firstname
        user.lastname = lastname
        user.save()
