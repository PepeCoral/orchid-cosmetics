from django.views import View
from django.shortcuts import render, redirect
from app.services.category_service import CategoryService


class ListCategoryView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category_service = CategoryService()

    def get(self, request):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        categories = self.category_service.list_categories()
        return render(request, "admin/categories/list.html", {"categories": categories})
