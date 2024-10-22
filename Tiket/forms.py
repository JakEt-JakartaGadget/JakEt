from django import forms
from Tiket.models import Tiket
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta

class TiketForm(forms.ModelForm):
    class Meta:
        model = Tiket
        fields = ["service_center", "service_date", "service_time", "specific_problems"]
        widgets = {
            'service_date': forms.DateInput(attrs={'type': 'date'}),
            'service_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


    def clean_service_time(self):
        service_time = self.cleaned_data['service_time']
        if not (time(8, 0) <= service_time <= time(21, 0)):
            raise ValidationError("Service time must be between 08:00 AM and 09:00 PM.")
        return service_time

    def clean_service_date(self):
        service_date = self.cleaned_data['service_date']
        now = datetime.now().date()
        last_login = self.request.user.last_login.date() if self.request.user.last_login else now
        if not (last_login <= service_date <= now + timedelta(days=30)):
            raise ValidationError("Service date must be within 30 days from your last login.")
        return service_date
