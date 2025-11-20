from django import forms

class BuyServiceForm(forms.Form):
    quantity = forms.IntegerField(
        label="Cantidad de sesiones",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'quantity-input',
            'min': '1'
        })
    )
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        
        if quantity <= 0:
            raise forms.ValidationError("La cantidad debe ser al menos 1 sesión.")
            
        return quantity