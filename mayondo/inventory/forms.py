from django import forms
from .models import Product, Stock

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Name',
            'type': 'Type',
            'description': 'Description',
        }
        help_texts = {
            'name': 'Enter the product name',
            'type': 'Select the product type',
            'description': 'Enter the product description',
        }
        error_messages = {
            'name': {'required': 'Please enter a product name'},
            'type': {'required': 'Please select a product type'},
            'description': {'required': 'Please enter a product description'},
        }
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [
            'product', 'supplier_name', 'quantity',
            'cost_price', 'selling_price',
            'quality', 'color', 'measurements'
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'supplier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quality': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'measurements': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'product': {'required': 'Please select a product'},
            'supplier_name': {'required': 'Please enter the supplier name'},
            'quantity': {'required': 'Please enter the quantity'},
            'cost_price': {'required': 'Please enter the cost price'},
            'selling_price': {'required': 'Please enter the selling price'},
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        cost_price = cleaned_data.get('cost_price')
        selling_price = cleaned_data.get('selling_price')

        if quantity is not None and quantity <= 0:
            self.add_error('quantity', "Quantity must be greater than zero")

        if cost_price is not None and selling_price is not None:
            if cost_price > selling_price:
                self.add_error('selling_price', "Selling price must be higher than cost price")

        return cleaned_data
