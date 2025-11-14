from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from app.models import User

from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "home.html")

@login_required
def profile(request):
    return render(request, "profile.html", {"user": request.user})


