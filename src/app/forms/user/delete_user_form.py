from django import forms

class DeleteUserForm(forms.Form):
    confirm_delete = forms.BooleanField(
        label="Confirmo que quiero eliminar mi cuenta permanentemente",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )