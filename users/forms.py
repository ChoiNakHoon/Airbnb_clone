from django import forms


class LoginForm(forms.Form):

    user = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
