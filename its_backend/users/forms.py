from django import forms
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    school = forms.CharField(max_length=100, required=True, help_text='Enter your school name')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'school']