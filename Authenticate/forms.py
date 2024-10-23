from django import forms
from django.contrib.auth.models import User
from .models import UserData

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

class FirstDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['profile_name', 'profile_picture', 'about', 'location', 'phone', 'email']

class EditDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['profile_name', 'profile_picture', 'about', 'location', 'phone', 'email', 'password']

