from IPLproject.models import *
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Enter username"})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "Enter password"})
    )
