from django.forms import ModelForm
from Authenticate.models import UserData

class ProfileForm(ModelForm):
    class Meta:
        model = UserData
        fields = ["profile_picture","profile_name", "username", "about", "phone", "email"]