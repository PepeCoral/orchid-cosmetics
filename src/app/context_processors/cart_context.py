from app.services.cart_item_service import CartService
from django.http import HttpRequest


class CartContext:
    def __init__(self):
        self.cart_service = CartService()

    def cart_amount_context(self,request:HttpRequest):
        total_amount = self.cart_service.get_total_amout(request.user)
        print(total_amount)
        return total_amount

def cart_amount_context(request:HttpRequest):

    context = CartContext()
    cart_items_amount = context.cart_amount_context(request)

    return {"cart_items_amount":cart_items_amount}