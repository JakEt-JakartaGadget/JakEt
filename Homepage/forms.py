from django import forms
from .models import Phone

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = [
            'brand', 'model', 'storage', 'ram', 'screen_size_inches',
            'camera_mp', 'battery_capacity_mAh', 'price_usd', 'price_inr',
            'rating', 'image_url', 'one_star', 'two_star', 'three_star',
            'four_star', 'five_star'
        ]
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'storage': forms.TextInput(attrs={'class': 'form-control'}),
            'ram': forms.TextInput(attrs={'class': 'form-control'}),
            'screen_size_inches': forms.NumberInput(attrs={'class': 'form-control'}),
            'camera_mp': forms.TextInput(attrs={'class': 'form-control'}),
            'battery_capacity_mAh': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_usd': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_inr': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'one_star': forms.NumberInput(attrs={'class': 'form-control'}),
            'two_star': forms.NumberInput(attrs={'class': 'form-control'}),
            'three_star': forms.NumberInput(attrs={'class': 'form-control'}),
            'four_star': forms.NumberInput(attrs={'class': 'form-control'}),
            'five_star': forms.NumberInput(attrs={'class': 'form-control'}),
        }
