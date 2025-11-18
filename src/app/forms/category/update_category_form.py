from django import forms
from django.core.validators import MaxLengthValidator
from app.models.category import Category

class UpdateCategoryForm(forms.ModelForm):
    
    name = forms.CharField(
        label="Nombre de la categoría",
        validators=[MaxLengthValidator(100, "Nombre de la categoría demasiado largo")]
    )
    
    class Meta:
        model = Category
        fields = ["name"]