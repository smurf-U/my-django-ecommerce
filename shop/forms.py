from django import forms
from .models import Customer


class AddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'street', 'street2', 'city', 'state', 'zipcode', 'country', 'email', 'mobile')
