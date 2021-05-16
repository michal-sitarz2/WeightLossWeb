from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import authenticate

from .models import Account


# Class extending the UserCreationForm provided by Django
# Defines the fields used to create a user.
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add valid email address')
    username = forms.CharField(min_length=5, max_length=30)

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

# Class which is a model form, and is responsible for checking if the user is valid when logging
# and authenticates the user
class AccountAuthenticationForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Invalid login")