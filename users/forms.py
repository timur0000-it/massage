from django.forms import ModelForm
from django import forms
from .models import CustomerUser
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ['username','email','photo','teacher','phone_number']

class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Имя пользователя')
    password = forms.CharField(max_length=150, required=True, label='Пароль')