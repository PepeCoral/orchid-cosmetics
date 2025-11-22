from django import forms
from django.core.validators import MaxLengthValidator
from app.models.order import DeliveryMethodOptions
from app.models.user import PaymentMethodOptions


class CheckoutForm(forms.Form):

    address = forms.CharField(
        label="Direccion",
        validators=[MaxLengthValidator(200,"Dirección demasiado larga")])

    delivery_method = forms.ChoiceField(
        label="Metodo de entrega",
        choices=DeliveryMethodOptions.choices)

    pay_method = forms.ChoiceField(
        label="Metodo de pago",
        choices=PaymentMethodOptions.choices)
