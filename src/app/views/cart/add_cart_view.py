from django.views import View
from django.shortcuts import redirect

from app.services.cart_item_service import CartService

class AddCartView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_service = CartService()

    def get(self, request, cart_id):
        self.cart_service.add_one_by_id(cart_id, request)
        return redirect("/cart")
