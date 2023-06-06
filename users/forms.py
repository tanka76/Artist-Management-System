import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from artist_management_system.utils import BaseForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout


from .models import AuthUser


class LoginForm(BaseForm,AuthenticationForm):
    class Meta:
        model = AuthUser
        fields = [
            "username",
            "password",
        ]

class CustomLoginForm(AuthenticationForm):

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Invalid email or password.')

        self.user = user
        return username

class UserCreateForm(BaseForm,forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ["first_name","last_name","phone_number","email","password","is_staff"]

    
    def clean_email(self):
        email = self.cleaned_data['email']
        if AuthUser.objects.filter(username=email).exists():
            raise ValidationError("Email with this user already exists")
        return email
    
    
    
    # def clean_phone_number(self):
    #     phone_number = self.cleaned_data['phone_number']
    #     pattern=r'^9\d{9}$'
    #     if not re.match(pattern, phone_number):
    #         raise ValidationError("Please enter valid phone number")
    #     return phone_number

    

