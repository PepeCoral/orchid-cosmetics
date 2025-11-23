from django import forms
from django.core.validators import MaxLengthValidator


class AnonymusSearchOrderForm(forms.Form):

    identifier = forms.CharField(
        label="Identificador de Pedido",
        validators=[MaxLengthValidator(150,"Identificador de Pedido demasiado largo")])
    
    def __init__(self, *args, **kwargs):
        self.max_stock = kwargs.pop('max_stock', None)
        super().__init__(*args, **kwargs)
    