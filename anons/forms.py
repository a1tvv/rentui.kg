from django import forms
from .models import Announcement

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'price', 'phone', 'address', 'image']
        widgets = {
            'image': MultipleFileInput(attrs={
                'class': 'form-control', 
                'multiple': True,  # Вот тут магия выбора через Shift
                'accept': 'image/*'
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }