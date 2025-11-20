from django import forms

class DeleteProductForm(forms.Form):
    confirm_delete = forms.BooleanField(
        label="Confirmo que quiero eliminar este producto permanentemente",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )