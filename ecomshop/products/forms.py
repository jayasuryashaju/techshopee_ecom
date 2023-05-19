from django import forms
from .models import Product, Category, Banner


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'brand', 'slug', 'image1', 'image2', 'image3', 'image4', 'description', 'price',
                  'stock_quantity']

    def __init__(self, *args, **kwargs):
        selected_category = kwargs.pop('selected_category', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].initial = selected_category


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ('product', 'name', 'image')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
