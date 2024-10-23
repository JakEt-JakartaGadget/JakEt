from django.forms import ModelForm
from ServiceCenter.models import ServiceCenter

class ServiceForm(ModelForm):
    class Meta:
        model = ServiceCenter
        fields = ["name", "address", "contact", "rating", "total_reviews"]