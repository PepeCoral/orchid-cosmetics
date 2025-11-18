from django.views import View
from django.shortcuts import render, redirect
from app.forms.user.delete_user_form import DeleteUserForm
from app.services.user_service import UserService

class DeleteUserView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    def get(self, request, user_id):
        if request.user.is_anonymous:
            return redirect("/")

        if request.user.id != int(user_id):
            return redirect("/")

        form = DeleteUserForm()
        return render(request, "user/delete.html", {"form": form})

    def post(self, request, user_id):
        if request.user.is_anonymous:
            return redirect("/")

        if request.user.id != int(user_id):
            return redirect("/")

        form = DeleteUserForm(request.POST)

        if not form.is_valid():
            return render(request, "user/delete.html", {"form": form})

        try:
            self.user_service.delete_user(user_id, request.user)
            from django.contrib.auth import logout
            logout(request)
            return redirect("/")
        except Exception as e:
            return render(
                request,
                "user/delete.html",
                {"form": form, "error": str(e)}
            )