from django.views import View
from django.shortcuts import render, redirect
from app.services.user_service import UserService


class ShowUserView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    def get(self, request, user_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        user = self.user_service.get_user_by_id(user_id)
        return render(request, "admin/users/detail.html", {"user": user})