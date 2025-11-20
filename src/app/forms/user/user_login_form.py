from django import forms
from app.models import User
from django.core.validators import MaxLengthValidator,EmailValidator, MinLengthValidator
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email", validators=[EmailValidator("Formato incorrecto")])
    password = forms.CharField(label="Introduzca su contraseña",
                               validators=[MinLengthValidator(5,"Contraseña demasiado corta")],
                               widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("No existe una cuenta con ese email.")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise forms.ValidationError("La contraseña es incorrecta.")

        self.user = user
        return self.cleaned_data