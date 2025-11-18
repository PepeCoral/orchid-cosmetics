from django.views import View
from django.shortcuts import render, redirect
from app.forms.category.update_category_form import UpdateCategoryForm
from app.services.category_service import CategoryService

class UpdateCategoryView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category_service = CategoryService()

    def get(self, request, category_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        category = self.category_service.get_category_by_id(category_id)
        form = UpdateCategoryForm(instance=category)

        return render(request, "admin/categories/update.html", {"form": form})

    def post(self, request, category_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        category = self.category_service.get_category_by_id(category_id)
        form = UpdateCategoryForm(request.POST, instance=category)

        if not form.is_valid():
            return render(request, "admin/categories/update.html", {"form": form})

        try:
            self.category_service.update_category(category_id, form.cleaned_data)
            return redirect("admin/categories")
        except Exception as e:
            return render(
                request,
                "admin/categories/update.html",
                {"form": form, "error": str(e)}
            )