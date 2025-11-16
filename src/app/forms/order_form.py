from django.forms import ModelForm
from django import forms
from app.models.category import Category
from django.core.validators import MaxLengthValidator,URLValidator, MinLengthValidator, DecimalValidator



class OrderForm(forms.Form):
    address = forms.CharField(label="Direccion de entrega",validators=[MaxLengthValidator(150,"Direccion de entrega demasiado larga")])
    payMethod = forms.CharField(label="Metodo de Pago", validators=[MaxLengthValidator(100,"Metodo de pago demasiado largo")])
    delivery_method = forms.CharField(label="Metodo de entrega", validators=[MaxLengthValidator(100,"Metodo de entrega demasiado largo")])
    
    def clean(self):
        cleaned_data = super().clean()
        
    