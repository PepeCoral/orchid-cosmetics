from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

from app.forms.user_register_form import UserRegisterForm
from app.services.user_service import UserService


class RegisterView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    def get(self, request):
        if not request.user.is_anonymous:
            return redirect("/profile")

        form = UserRegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        if not request.user.is_anonymous:
            return redirect("/profile")

        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "register.html", {"form": form})

        try:
            user = self.user_service.create_user(form.cleaned_data)
            auth_login(request, user)
            return redirect("/profile")
        except Exception as e:
            return render(
                request,
                "register.html",
                {"form": form, "error": "An unexpected error occurred."}
            )
