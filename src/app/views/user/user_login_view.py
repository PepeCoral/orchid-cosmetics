from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView 
from app.services.user_service import UserService
from app.forms.user.user_login_form import UserLoginForm
from django.contrib.auth import login

class UserLoginView(LoginView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()
        
    def get(self, request):
        if not request.user.is_anonymous:
            return redirect("/profile")
        
        form = UserLoginForm()
        return render(request, "user/login.html", {"form":form})

    def post(self, request):
        if not request.user.is_anonymous:
            return redirect("/profile")
        
        form = UserLoginForm(request.POST)

        if not form.is_valid():
            return render(request, "user/login.html",{"form":form})
        
        try:
            user = self.user_service.authenticate_user(form.cleaned_data)
            login(request,user)
            return redirect("/profile")
        except Exception as e:
            return render(
                request,
                "user/login.html",
                {"form":form, "error":str(e)}
            )