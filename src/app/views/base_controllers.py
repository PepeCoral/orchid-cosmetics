from django.shortcuts import render, HttpResponse
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from app.models import User


def home(request):
    return render(request, "home.html")


def profile(request):
    items = User.objects.all()
    return render(request, "profile.html", {'users': items})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)

        print(user)
        if user is not None:
            # Iniciar sesión
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect("home")  # Redirige a la página principal
        else:
            # Error de credenciales
            messages.error(request, "Usuario o contraseña incorrectos")
        
    # Si es GET o falló el login, renderiza el formulario
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")
