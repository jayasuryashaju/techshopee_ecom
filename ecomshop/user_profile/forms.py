from datetime import date

from django import forms
from django.contrib.auth import get_user_model

from .models import UserAddress
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

User = get_user_model()


# class UserAddressForm(forms.ModelForm):
#     class Meta:
#         model = UserAddress
#         fields = ['full_name', 'address', 'city', 'state', 'zip_code', 'phone', 'email']
#         labels = {
#             'full_name': 'Full Name',
#             'address': 'Address',
#             'city': 'City, State',
#             'zip_code': 'Zip Code',
#             'phone': 'Phone',
#             'email': 'Email'
#         }
#         widgets = {
#             'full_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'address': forms.TextInput(attrs={'class': 'form-control'}),
#             'city': forms.TextInput(attrs={'class': 'form-control'}),
#             'state': forms.TextInput(attrs={'class': 'form-control'}),
#             'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'})
#         }

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['full_name', 'address', 'city', 'state', 'zip_code', 'phone', 'email']
        labels = {
            'full_name': 'Full Name',
            'address': 'Address',
            'city': 'City',
            'state': 'State',
            'zip_code': 'Zip Code',
            'phone': 'Phone',
            'email': 'Email'
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your State'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your zip code'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] += ' user-address-input'



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'email', 'phone_number']
