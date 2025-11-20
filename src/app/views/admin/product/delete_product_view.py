# app/views/admin/product/delete_product_view.py
from django.views import View
from django.shortcuts import render, redirect
from app.forms.product.delete_product_form import DeleteProductForm
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

        product = self.product_service.get_product_by_id(product_id)
        form = DeleteProductForm()
        return render(request, "admin/products/delete.html", {"form": form, "product": product})

    def post(self, request, product_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        form = DeleteProductForm(request.POST)

        if not form.is_valid():
            product = self.product_service.get_product_by_id(product_id)
            return render(request, "admin/products/delete.html", {"form": form, "product": product})

        try:
            self.product_service.delete_product(product_id)
            return redirect("admin/products")
        except Exception as e:
            product = self.product_service.get_product_by_id(product_id)
            return render(
                request,
                "admin/products/delete.html",
                {"form": form, "product": product, "error": str(e)}
            )