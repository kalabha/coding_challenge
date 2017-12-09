from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Otp

CustomUser = get_user_model()


class SignUpForm(ModelForm):
    class Meta:
        model = CustomUser
        widgets = {
            "first_name": forms.TextInput(attrs={'class': "form-control", 'required': "required"}),
            "last_name": forms.TextInput(attrs={'class': "form-control", 'required': "required"}),
            "gender": forms.Select(attrs={'class': "form-control"}),
            "phone_number": forms.NumberInput(attrs={'class': "form-control"}),
            "email": forms.EmailInput(attrs={'class': "form-control"}),
        }
        fields = ['first_name', 'last_name', 'gender', 'phone_number', 'email']


class OtpVerificationForm(ModelForm):
    class Meta:
        model = Otp
        widgets = {
            "code": forms.TextInput(attrs={'class': "form-control", }),

        }
        fields = ['code', 'user']
