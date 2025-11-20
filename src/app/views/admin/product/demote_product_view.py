from django.views import View
from django.shortcuts import render, redirect
from app.services.product_service import ProductService


class DemoteProductView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def post(self, request, product_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")
        
        products = self.product_service.get_all_products()
        try:
            self.product_service.demote_product(product_id)
            return redirect(f"/admin/products")
        except Exception as e:
            return render(
                request,
                "admin/products/list.html",
                {"productos": products, "error": str(e)}
            )