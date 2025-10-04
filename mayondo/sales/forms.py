from django import forms
from .models import Sale, SaleItem
from django.forms import inlineformset_factory
from inventory.models import Stock

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name', 'payment_type', 'transport_required']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'transport_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_customer_name(self):
        customer_name = self.cleaned_data.get('customer_name')
        if not customer_name:
            raise forms.ValidationError("Customer name is required")
        if len(customer_name) < 3:
            raise forms.ValidationError("Customer name must be at least 3 characters long")
        return customer_name


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero")
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data.get('unit_price')
        if unit_price is None or unit_price <= 0:
            raise forms.ValidationError("Unit price must be greater than zero")
        return unit_price

    def clean_product(self):
        product = self.cleaned_data.get('product')
        if product is None:
            raise forms.ValidationError("Please select a product")
        return product

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get("product")
        unit_price = cleaned_data.get('unit_price')
        if quantity is not None and unit_price is not None:
            total_price = quantity * unit_price
            cleaned_data['total_price'] = total_price

        if product and quantity:
            stock = Stock.objects.filter(product=product).first()
            if stock and stock.quantity < quantity:
               raise forms.ValidationError(
                f"Not enough stock available for {product.name}. "
                f"Available: {stock.quantity}, Requested: {quantity}"
                )
        return cleaned_data
    
SaleItemFormSet = inlineformset_factory(
    Sale, SaleItem,
    form=SaleItemForm,
    extra=1,  # show at least 1 blank form
    can_delete=True
) 