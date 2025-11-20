from django import forms


class BuyProductForm(forms.Form):

    quantity = forms.IntegerField(
        label="Cantidad",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'quantity-input',
            'min': '1'
        })
    )
    
    def __init__(self, *args, **kwargs):
        self.max_stock = kwargs.pop('max_stock', None)
        super().__init__(*args, **kwargs)
        
        if self.max_stock:
            self.fields['quantity'].widget.attrs['max'] = str(self.max_stock)
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if self.max_stock and quantity > self.max_stock:
            raise forms.ValidationError(
                f"No hay suficiente stock. Solo quedan {self.max_stock} unidades disponibles."
            )
        return quantity