from django.views import View
from django.shortcuts import render, redirect
from app.services.product_service import ProductService


class ListProductView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def get(self, request):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        product = self.product_service.get_all_products()
        
        return render(request, "admin/products/list.html", {"productos": product})
