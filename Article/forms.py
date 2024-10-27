from django import forms
from .models import Artikel

class ArtikelForm(forms.ModelForm):
    class Meta:
        model = Artikel
        fields = ['title', 'content', 'image_url', 'source']
