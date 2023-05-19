from django import forms

from cart.models import Order, ProductOffer, CategoryOffer


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=1)


class OrderForm(forms.ModelForm):
    shipping_options = forms.ChoiceField(
        choices=[('free_shipping', 'Free Shipping (₹0)'), ('faster_shipping', 'Faster Shipping(₹100)')],
        widget=forms.RadioSelect(attrs={'name': 'shipping_options'})
    )

    class Meta:
        model = Order
        fields = ['quantity', 'shipping_address', 'phone_number', 'shipping_options']

    quantity = forms.IntegerField(min_value=1, max_value=100)
    shipping_address = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)


class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = ('category', 'name', 'discount', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'end_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryOfferForm, self).__init__(*args, **kwargs)

        self.fields['discount'].widget.attrs['placeholder'] = 'Enter the discount percentage'

    # additional form validation and customization if needed


class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ('name', 'product', 'discount', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'end_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(ProductOfferForm, self).__init__(*args, **kwargs)

        self.fields['discount'].widget.attrs['placeholder'] = 'Enter the discount percentage'
