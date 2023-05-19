from django.utils import timezone
from django import forms
from django.contrib.auth.models import User

from cart.models import Coupon


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            'code',
            'description',
            'discount_value',
            'minimum_purchase',
            'maximum_discount',
            'active',
            'valid_from',
            'valid_to',
        ]
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_to = cleaned_data.get('valid_to')

        if valid_from and valid_to and valid_from >= valid_to:
            raise forms.ValidationError("Valid from date must be before valid to date.")

        return cleaned_data

    def clean_discount_value(self):
        discount_value = self.cleaned_data['discount_value']
        if discount_value <= 0:
            raise forms.ValidationError("Discount value must be greater than zero.")
        return discount_value

    def clean_maximum_discount(self):
        maximum_discount = self.cleaned_data['maximum_discount']
        if maximum_discount and maximum_discount <= 0:
            raise forms.ValidationError("Maximum discount must be greater than zero.")
        return maximum_discount

    def clean_minimum_purchase(self):
        minimum_purchase = self.cleaned_data['minimum_purchase']
        if minimum_purchase and minimum_purchase <= 0:
            raise forms.ValidationError("Minimum purchase must be greater than zero.")
        return minimum_purchase

    def clean_valid_from(self):
        valid_from = self.cleaned_data['valid_from']
        if valid_from < timezone.now():
            raise forms.ValidationError("Valid from date must be in the future.")
        return valid_from
