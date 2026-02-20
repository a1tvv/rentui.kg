from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    # Указываем обычное поле без attrs['multiple'] здесь
    image = forms.ImageField(
        label="Фотографии",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        required=False
    )

    class Meta:
        model = Announcement
        fields = ['title', 'description', 'price', 'phone', 'address', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # А вот тут мы принудительно втыкаем multiple в обход валидатора виджета
        self.fields['image'].widget.attrs.update({'multiple': True})