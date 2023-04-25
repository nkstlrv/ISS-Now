from .models import Location
from django import forms


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('user', 'city', 'country')

        widgets = {

            'user': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user_id', 'type': 'hidden'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Country'}),
        }