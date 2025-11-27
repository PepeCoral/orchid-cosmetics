from django.views import View
from django.shortcuts import redirect

from app.services.category_service import CategoryService


class DeleteCategoryView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category_service = CategoryService()

    def get(self, request, category_id):
        return redirect("/")

        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        self.category_service.delete_category(category_id)
        return redirect("admin/categories")
