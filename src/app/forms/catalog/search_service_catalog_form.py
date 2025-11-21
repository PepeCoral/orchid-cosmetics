from django import forms
from app.models.category import Category

class SearchServiceCatalogForm(forms.Form):
    name = forms.CharField(
        label="Nombre",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre...'
        })
    )

    department = forms.CharField(
        label="Departamento",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Departamento...'
        })
    )

    min_price = forms.DecimalField(
        label="Precio mínimo",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo €'
        })
    )

    max_price = forms.DecimalField(
        label="Precio máximo",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Máximo €'
        })
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label="Categorías",
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
