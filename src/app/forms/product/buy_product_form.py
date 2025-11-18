from django import forms


class BuyProductForm(forms.Form):

    quantity = forms.IntegerField(
        label="Cantidad",
        required=True,
        min_value=0,
        initial=1)
