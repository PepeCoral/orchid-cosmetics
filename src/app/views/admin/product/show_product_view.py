from django.views import View
from django.shortcuts import render, redirect
from app.services.product_service import ProductService


class ShowProductView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def get(self, request, product_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        product = self.product_service.get_product_by_id(product_id)
        categories = product.categories.all()
        return render(request, "admin/products/detail.html", {"product": product, "categories": categories})
