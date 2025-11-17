from django.forms import ModelForm
from django import forms
from app.models import Category
from django.core.validators import MaxLengthValidator,MinValueValidator



class ServiceForm(forms.Form):
    name = forms.CharField(label="Nombre del servicio",
                           validators=[MaxLengthValidator(150,"Nombre del servicio demasiado largo")])
    
    description = forms.CharField(label="Descripcion", 
                                  validators=[MaxLengthValidator(300,"Description too long")])
    
    price = forms.DecimalField(label="Precio", decimal_places=2, min_value=0.0,
                               validators=[MinValueValidator(0.0,"El precio debe ser mayor o igual que 0.0")])
    
    duration_minutes = forms.IntegerField(label="Duracion", min_value=0)
    
    department = forms.CharField(label="Departamento",
                                 validators=[MaxLengthValidator(200,"Departament too long")],required=False)
    image_url = forms.ImageField(label="Imagen del servicio",required=False)
    
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                      widget=forms.SelectMultiple,
                                      required=False,
                                      label="Categorias")
    
    def clean(self):
        cleaned_data = super().clean()
        
    