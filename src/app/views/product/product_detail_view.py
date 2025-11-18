from django.views import View
from django.shortcuts import render, redirect

from app.services.product_service import ProductService
from app.forms.product.buy_product_form import BuyProductForm

class ProductDetailView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def get(self, request, product_id):
        form = BuyProductForm()
        product = self.product_service.get_product_by_id(product_id)
        return render(request, "product/detail.html", {"form": form, "product":product})

    def post(self, request,product_id):

        if request.user.is_anonymous:
            return redirect("/login")

        product = self.product_service.get_product_by_id(product_id)
        form = BuyProductForm(request.POST)

        if not form.is_valid():
            return render(request, "product/detail.html", {"form": form, "product": product})

        try:
            pass
            return redirect("/cash")
        except Exception as e:
            return render(
                request,
                "product/detail.html",
                {"form": form, "error": str(e), "product": product}
            )
