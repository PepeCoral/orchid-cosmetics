from django.urls import path
from app.views.checkout.checkout_view import CheckoutView
from app.views.order.list_order_user_view import ListOrderUserView
from app.views.items.list_user_items_view import ListItemView
from app.views.order.anonymous_search_order_view import AnonymousSearchOrderView

urlpatterns = [
  path("checkout/", CheckoutView.as_view(), name="checkout"),
  path("orders", ListOrderUserView.as_view(), name="orders"),
  path("orders/items/<int:order_id>", ListItemView.as_view(), name="orders/items"),
  path("orders/anonymous_search/", AnonymousSearchOrderView.as_view(), name="orders/anonymous_search"),
]
