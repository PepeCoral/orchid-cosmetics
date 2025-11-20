from django import forms
from app.models import User
from django.core.validators import MaxLengthValidator,EmailValidator, MinLengthValidator
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email", validators=[EmailValidator("Formato incorrecto")])
    password = forms.CharField(label="Introduzca su contraseña",
                               validators=[MinLengthValidator(5,"Contraseña demasiado corta")],
                               widget=forms.PasswordInput())

    