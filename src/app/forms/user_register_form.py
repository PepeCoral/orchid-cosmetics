from django.forms import ModelForm
from django import forms
from app.models import User
from django.core.validators import MaxLengthValidator,EmailValidator, MinLengthValidator



class UserRegisterForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario",validators=[MaxLengthValidator(150,"Nombre de usuario demasiado largo")])
    first_name = forms.CharField(label="Nombre/s", validators=[MaxLengthValidator(100,"First name too long")])
    last_name = forms.CharField(label="Apellidos", validators=[MaxLengthValidator(100,"Last name too long")])
    email = forms.EmailField(label="Email", validators=[EmailValidator("Formato incorrecto")])
    address = forms.CharField(label="Dirección",validators=[MaxLengthValidator(200,"Address too long")],required=False)
    pay_method = forms.CharField(label="Método de pago", required=False)
    password = forms.CharField(label="Introduzca una contraseña", 
                               validators=[MinLengthValidator(6,"Contraseña demasiado corta")], 
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Escriba de nuevo la contraseña", 
                                       validators=[MinLengthValidator(6,"Contraseña demasiado corta")], 
                                       widget=forms.PasswordInput())


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]

        if password and confirm_password:
            if password != confirm_password:
                self.add_error("confirm_password", "Las contraseñas no coinciden")
            if len(password) < 6 or len(confirm_password) < 6:
                self.add_error("confirm_password", "la contraseña debe tener mas de 6 caracteres")


        if email and User.objects.filter(email=email).exists():
            self.add_error("email", "el email ya esta en uso")

        if username and User.objects.filter(username=username).exists():
            self.add_error("username", "el nombre de usuario ya esta en uso")

