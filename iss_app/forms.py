from django import forms
from django.core.exceptions import ValidationError

from .models import Location, Notify
from calculations.geocode_name import check_if_exist


class CityField(forms.CharField):
    def clean(self, value):

        value = super().clean(value)

        if check_if_exist(value):
            return value
        else:
            raise ValidationError('Invalid City name')


class CountryField(forms.CharField):
    def clean(self, value):

        value = super().clean(value)

        if check_if_exist(value):
            return value
        else:
            raise ValidationError('Invalid Country name')


class LocationForm(forms.ModelForm):
    city = CityField()
    country = CountryField()

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




