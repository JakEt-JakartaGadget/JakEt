from django import forms
from django.forms import ModelForm
from .models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Tulis review Anda di sini...'}),
        }

    rating_choices = [
        (1, '★ 1'),
        (2, '★ 2'),
        (3, '★ 3'),
        (4, '★ 4'),
        (5, '★ 5'),
    ]
    rating = forms.ChoiceField(
        choices=rating_choices,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'})
    )
