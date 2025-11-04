from django.shortcuts import render, HttpResponse
from .models import User


def home(request):
    return render(request, "home.html")


def profile(request):
    items = User.objects.all()
    return render(request, "profile.html", {'users': items})
