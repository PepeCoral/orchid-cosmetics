from django.urls import path
from app.views.checkout.checkout_view import CheckoutView

urlpatterns = [
  path("checkout/", CheckoutView.as_view(), name="checkout")
]
