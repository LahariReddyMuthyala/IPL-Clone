from IPLproject.models import *
from django import forms


class SignUpForm(forms.Form):
    firstname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Enter first name"})
    )
    lastname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Enter last name "})
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Enter username"})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "Enter password"})
    )