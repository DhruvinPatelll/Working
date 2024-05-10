from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profile_image']
        
class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1']