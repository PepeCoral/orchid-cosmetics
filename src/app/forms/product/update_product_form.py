from django import forms
from app.models.category import Category
from app.models.product import Product
from django.core.validators import MaxLengthValidator


class UpdateProductForm(forms.ModelForm):

    name = forms.CharField(
        label="Nombre del producto",
        validators=[MaxLengthValidator(150, "Nombre del producto demasiado largo")]
    )

    description = forms.CharField(
        label="Descripción",
        validators=[MaxLengthValidator(300, "Descripción demasiado larga")]
    )

    fabricator = forms.CharField(
        label="Fabricante",
        validators=[MaxLengthValidator(200, "Fabricator too long")],
        required=False
    )

    image_url = forms.ImageField(
        label="Imagen del producto",
        required=False
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple,
        required=False,
        label="Categorías"
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "stock",
            "fabricator",
            "image_url",
            "categories",
        ]
