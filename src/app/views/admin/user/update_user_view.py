from django.views import View
from django.shortcuts import render, redirect
from app.forms.user.update_user_form import UpdateUserForm
from app.services.user_service import UserService


class UpdateUserView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    def get(self, request, user_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        user = self.user_service.get_user_by_id(user_id)

        if user.is_superuser:
            return redirect("/")
        
        form = UpdateUserForm(instance=user)

        return render(request, "admin/users/update.html", {"user": user, "form": form})
    
    def post(self, request, user_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        user = self.user_service.get_user_by_id(user_id)
        
        if user.is_superuser:
            return redirect("/")
        
        form = UpdateUserForm(request.POST, instance=user)

        if not form.is_valid():
            return render(request, "admin/users/update.html", {"user": user, "form": form})

        try:
            self.user_service.update_user(user_id, form.cleaned_data, request.user)
            return redirect(f"/admin/users/show/{user_id}/")
        except Exception as e:
            return render(
                request,
                "admin/users/update.html",
                {"user": user, "form": form, "error": str(e)}
            )