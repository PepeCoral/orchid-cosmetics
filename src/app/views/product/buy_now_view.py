from django.views import View
from django.shortcuts import render, redirect
from app.services.product_service import ProductService
from app.services.cart_item_service import CartService
from app.forms.product.buy_product_form import BuyProductForm

class BuyNowView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()
        self.cart_service = CartService()


    def post(self, request, product_id):
        product = self.product_service.get_product_by_id(product_id)
        categories = product.categories.all()

        form = BuyProductForm(request.POST, max_stock=product.stock)

        if not form.is_valid():
            return render(request, "product/detail.html", {
                "form": form,
                "product": product,
                "categories": categories
            })

        try:

            quantity = form.cleaned_data['quantity']
            self.cart_service.add_item(request, product, quantity)

            return redirect("/checkout")
        except Exception as e:
            return render(
                request,
                "product/detail.html",
                {
                    "form": form,
                    "error": str(e),
                    "product": product,
                    "categories": categories
                }
            )