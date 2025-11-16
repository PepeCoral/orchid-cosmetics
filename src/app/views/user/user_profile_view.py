from django.views import View
from django.shortcuts import render, redirect
from app.services.user_service import UserService


class UserProfileView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    def get(self, request):
      return render(request, "profile.html")
