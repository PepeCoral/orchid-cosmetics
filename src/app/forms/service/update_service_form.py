from django import forms
from app.models.service import Service
from app.models.category import Category
from django.core.validators import MinValueValidator, MaxLengthValidator

class UpdateServiceForm(forms.ModelForm):
    name = forms.CharField(
        label="Nombre del servicio",
        validators=[MaxLengthValidator(100, "Nombre del servicio demasiado largo")]
    )
    
    description = forms.CharField(
        label="Descripción",
        widget=forms.Textarea
    )
    
    price = forms.DecimalField(
        label="Precio",
        decimal_places=2,
        min_value=0,
        validators=[MinValueValidator(0.0)]
    )
    
    duration_minutes = forms.IntegerField(
        label="Duración (minutos)",
        min_value=0,
        validators=[MinValueValidator(0)]
    )
    
    department = forms.CharField(
        label="Departamento",
        validators=[MaxLengthValidator(100, "Departamento demasiado largo")]
    )
    
    image_url = forms.ImageField(
        label="Imagen del servicio",
        required=False
    )
    
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple,
        required=False,
        label="Categorías"
    )

    class Meta:
        model = Service
        fields = [
            "name",
            "description", 
            "price",
            "duration_minutes",
            "department",
            "image_url",
            "categories",
        ]