from django.views import View
from django.shortcuts import  redirect
from django.contrib.auth import  logout
from app.services.user_service import UserService


class UserLogoutView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
      logout(request)
      return redirect("/")
