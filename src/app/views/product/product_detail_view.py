from django.views import View
from django.shortcuts import render, redirect

from app.services.product_service import ProductService
from app.forms.product.buy_product_form import BuyProductForm
from app.services.cart_item_service import CartService

class ProductDetailView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()
        self.cart_service = CartService()

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
            self.cart_service.add_item(request.user, product, form.cleaned_data["quantity"])
            return redirect("/cart")
        except Exception as e:
            return render(
                request,
                "product/detail.html",
                {"form": form, "error": str(e), "product": product}
            )
