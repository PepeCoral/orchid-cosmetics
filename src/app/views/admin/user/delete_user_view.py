# app/views/admin/product/delete_product_view.py
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

        if not request.user.is_superuser:
            return redirect("/")

        user = self.user_service.get_user_by_id(user_id)
        
        # if user.is_superuser:
        #     return redirect("/")
        
        form = DeleteUserForm()
        return render(request, "admin/users/delete.html", {"form": form, "user": user})

    def post(self, request, user_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        user = self.user_service.get_user_by_id(user_id)

        if user.is_superuser:
            return redirect("/")
        
        form = DeleteUserForm(request.POST)

        if not form.is_valid():
            return render(request, "admin/users/delete.html", {"form": form, "user": user})
        try:
            self.user_service.delete_user(user_id, request.user)
            return redirect("admin/users")
        except Exception as e:
            return render(
                request,
                "admin/users/delete.html",
                {"form": form, "user": user, "error": str(e)}
            )