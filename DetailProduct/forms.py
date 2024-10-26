from django import forms
from django.forms import ModelForm
from .models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'content': forms.Textarea(attrs={'placeholder': 'Tulis review Anda di sini...'}),
        }

        