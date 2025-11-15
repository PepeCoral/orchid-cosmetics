from django.forms import ModelForm
from django import forms
from django.core.validators import MaxLengthValidator,URLValidator, MinLengthValidator, DecimalValidator



class ProductForm(forms.Form):
    name = forms.CharField(label="Nombre del servicio",validators=[MaxLengthValidator(150,"Nombre del servicio demasiado largo")])
    description = forms.CharField(label="Descripcion", validators=[MaxLengthValidator(300,"Description too long")])
    price = forms.DecimalField(label="Precio", decimal_places=2)
    stock = forms.IntegerField(label="Stock", required=True)
    fabricator = forms.CharField(label="Fabricante",validators=[MaxLengthValidator(200,"Departament too long")],required=False)
    image = forms.ImageField(label="Imagen del servicio",required=False)
    category = forms.CharField(label="Introduzca una categoria", required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        
    