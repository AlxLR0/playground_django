from django import forms
from .models import Review

class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, 
        max_value=5,
        widget = forms.NumberInput(attrs={
            'placeholder': 'Puntuación del 1 al 5',
            'class': 'form-control',
        })
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe tu reseña',
            'class': 'form-control',
            'rows': 3,
        })
    )