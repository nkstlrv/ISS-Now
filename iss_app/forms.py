from django import forms

from .models import Location, Notify


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('user', 'city', 'country')

        widgets = {

            'user': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user_id', 'type': 'hidden'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Country'}),
        }


class NotifyForm(forms.ModelForm):
    class Meta:
        model = Notify
        fields = ('user',)

        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user_id', 'type': 'hidden'}),
        }
