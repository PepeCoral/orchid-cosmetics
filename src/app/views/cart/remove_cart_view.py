from django.views import View
from django.shortcuts import redirect

from app.services.cart_item_service import CartService

class RemoveCartView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_service = CartService()

    def get(self, request, cart_id):
        self.cart_service.remove_one_by_id(cart_id, request)
        return redirect("/cart")
