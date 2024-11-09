from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        exclude = ['date_joined']  # Make sure date_joined is excluded
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
