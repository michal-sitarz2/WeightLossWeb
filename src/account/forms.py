from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import authenticate

from .models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add valid email address')
    weight = forms.FloatField(validators=[MinValueValidator(1), MaxValueValidator(400)])
    height = forms.FloatField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    weight_goal = forms.FloatField(validators=[MinValueValidator(1), MaxValueValidator(400)])
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2', 'height', 'weight', 'weight_goal')


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")