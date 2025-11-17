from django import forms
from app.models.user import User
from django.core.validators import MaxLengthValidator

class UpdateUserForm(forms.ModelForm):

    first_name = forms.CharField(
        label="Nombre",
        validators=[MaxLengthValidator(100, "Nombre demasiado largo")]
    )

    last_name = forms.CharField(
        label="Apellidos",
        validators=[MaxLengthValidator(100, "Apellidos demasiado largos")]
    )

    email = forms.EmailField(
        label="Correo electrónico"
    )

    username = forms.CharField(
        label="Nombre de usuario",
        validators=[MaxLengthValidator(150, "Nombre de usuario demasiado largo")]
    )

    address = forms.CharField(
        label="Dirección",
        validators=[MaxLengthValidator(200, "Dirección demasiado larga")],
        required=False
    )

    pay_method = forms.CharField(
        label="Método de pago",
        validators=[MaxLengthValidator(50, "Método de pago demasiado largo")],
        required=False
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        required=False,
        help_text="Dejar en blanco si no quieres cambiar la contraseña"
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name", 
            "email",
            "username",
            "address",
            "pay_method",
            "password",
        ]