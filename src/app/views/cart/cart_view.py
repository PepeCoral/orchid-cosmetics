from django.views import View
from django.shortcuts import render
from app.services.cart_item_service import CartService
from app.models.product import Product
from app.models.service import Service

class CartView(View):
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

        return render(request, "cart/cart.html", {
            "products": products,
            "services": services,
            "total": max(0.5,total)
        })
