from django.views import View
from django.shortcuts import redirect

from app.services.product_service import ProductService

class DeleteProductView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def get(self, request, product_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        self.product_service.delete_product(product_id)
        return redirect("admin/products")
