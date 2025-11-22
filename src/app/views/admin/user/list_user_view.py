from django.views import View
from django.shortcuts import render, redirect
from app.models.user import RoleOptions
from app.services.user_service import UserService


class ListUserView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    def get(self, request):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        users = self.user_service.get_all_users()

        role = RoleOptions.USER
        
        return render(request, "admin/users/list.html", {"usuarios": users, "role": role})