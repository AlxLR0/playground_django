from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    would_recommend = forms.BooleanField(required=False, label="¿Recomendarías este libro?")
    
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'placeholder': 'Puntuación del 1 al 5',
                'class': 'form-control',
                'min': 1,
                'max': 5,
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Escribe tu reseña',
                'class': 'form-control',
                'rows': 3,
            }),
        }
