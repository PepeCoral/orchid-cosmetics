from django.views import View
from django.shortcuts import render, redirect
from app.forms.category.create_category_form import CategoryForm
from app.services.category_service import CategoryService

class CreateCategoryView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category_service = CategoryService()

    def get(self, request):
        return redirect("/")

        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        form = CategoryForm()
        return render(request, "admin/categories/create.html", {"form": form})

    def post(self, request):
        return redirect("/")

        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        form = CategoryForm(request.POST)

        if not form.is_valid():
            return render(request, "admin/categories/create.html", {"form": form})

        try:
            self.category_service.create_category(form.cleaned_data)
            return redirect("admin/categories")
        except Exception as e:
            return render(
                request,
                "admin/categories/create.html",
                {"form": form, "error": str(e)}
            )
