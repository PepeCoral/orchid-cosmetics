from django.urls import path
from app.views.cart.cart_view import CartView
from app.views.cart.add_cart_view import AddCartView
from app.views.cart.remove_cart_view import RemoveCartView
from app.views.cart.delete_cart_view import DeleteCartView

urlpatterns = [
    path("cart", CartView.as_view(), name="cart"),
    path("cart/add/<int:cart_id>", AddCartView.as_view(), name="cart/add"),
    path("cart/remove/<int:cart_id>", RemoveCartView.as_view(), name="cart/remove"),
    path("cart/delete/<int:cart_id>", DeleteCartView.as_view(), name="cart/delete"),
]
