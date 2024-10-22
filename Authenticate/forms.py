from django.forms import ModelForm
from .models import UserData

class UserDataForm(ModelForm):
    class Meta:
        model = UserData
        fields = ['profile_name','username','profile_picture','about','location','phone','email','password']

class EditDataForm(ModelForm):
    class Meta:
        model = UserData
        fields = ['profile_name','username','profile_picture','about','location','phone','email','password']