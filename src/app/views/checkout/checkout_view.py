from django.views import View
from django.shortcuts import render
from app.forms.checkout.checkout_form import CheckoutForm
from app.services.user_service import UserService
from app.services.cart_item_service import CartService
from app.models.product import Product
from app.models.service import Service

class CheckoutView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_service = CartService()

    def get(self, request):
        cart_items = self.cart_service.get_cart_items(request)

        products = []
        services = []
        for item in cart_items:
            if isinstance(item.item, Product):
                products.append(item)
            elif isinstance(item.item, Service):
                services.append(item)

        total = self.cart_service.get_total(request)

        form = CheckoutForm()
        return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total})

    def post(self, request):

        cart_items = self.cart_service.get_cart_items(request)

        products = []
        services = []
        for item in cart_items:
            if isinstance(item.item, Product):
                products.append(item)
            elif isinstance(item.item, Service):
                services.append(item)

        total = self.cart_service.get_total(request)

        form = CheckoutForm(request.POST)

        if not form.is_valid():
            return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total})


        try:
            pass
        except Exception as e:
            return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total, "error": e})
