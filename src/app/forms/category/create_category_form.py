from django.forms import ModelForm
from django import forms
from app.models import Category
from django.core.validators import MaxLengthValidator,URLValidator, MinLengthValidator, DecimalValidator



class CategoryForm(forms.Form):
    name = forms.CharField(label="Nombre de la categoria",validators=[MaxLengthValidator(150,"Nombre de la categoria demasiado larga")])

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data['name']

        if Category.objects.filter(name=name).exists():
            self.add_error("name","Ya existe una categoria con ese nombre")
