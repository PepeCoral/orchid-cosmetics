from django.views import View
from django.shortcuts import render, redirect
from app.services.user_service import UserService


class AdminPanelView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    def get(self, request):

      if request.user.is_anonymous:
        return redirect("/")

      if not request.user.is_superuser:
         return redirect("/")

      return render(request, "admin/panel.html")
