<<<<<<< HEAD
from django.shortcuts import render, HttpResponse
from .models import User


def home(request):
    return render(request, "home.html")


def profile(request):
    items = User.objects.all()
    return render(request, "profile.html", {'users': items})
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 56922cb6739d34c05bdc57d56701856416f7f594
