from django import forms

class DeleteServiceForm(forms.Form):
    confirm_delete = forms.BooleanField(
        label="Confirmo que quiero eliminar este servicio permanentemente",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )