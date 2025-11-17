from django import forms
from app.models.category import Category
from django.core.validators import MaxLengthValidator


class SearchCatalogForm(forms.Form):

    name = forms.CharField(
        label="Nombre del producto",
        validators=[MaxLengthValidator(150,"Nombre del producto demasiado largo")],
        required=False)

    min_price = forms.DecimalField(
        label="Precio Mínimo",
        decimal_places=2,
        required=False,
        min_value=0)

    max_price = forms.DecimalField(
        label="Precio Máximo",
        decimal_places=2,
        required=False,
        min_value=0)

    fabricator = forms.CharField(
        label="Fabricante",
        validators=[MaxLengthValidator(200,"Fabricator too long")],
        required=False)

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple,
        required=False,
        label="Categorias")
