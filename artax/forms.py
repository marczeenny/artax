from django import forms
from phonenumber_field.formfields import PhoneNumberField


class ClientForm(forms.Form):
    name = forms.CharField(max_length=350)
    email = forms.EmailField()
    person_in_charge = forms.CharField(max_length=200)
    mobile_number = PhoneNumberField()
    landline_number = PhoneNumberField()
    address = forms.CharField(widget=forms.Textarea)
    web_address = forms.URLField()
