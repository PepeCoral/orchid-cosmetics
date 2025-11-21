from django.views import View
from django.shortcuts import render, redirect
import stripe
from django.http import HttpRequest
from django.conf import settings
from app.services.cart_item_service import CartService
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateSessionStripeView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_service = CartService()

    def get(self,request:HttpRequest):
        if request.user.is_anonymous:
            return redirect("/")

        success_url = reverse(viewname="checkout_success")
        cancel_url = reverse(viewname="checkout_cancel")

        cart_items_stripefied =[item.stripify() for item in self.cart_service.get_cart_items(request.user)]

        if len(cart_items_stripefied) == 0:
            return redirect("/cart")

        session = stripe.checkout.Session.create(
            payment_method_types=["card","paypal","amazon_pay"],
            line_items=cart_items_stripefied,
            mode="payment",
            success_url=request.build_absolute_uri(
                success_url)+ '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(cancel_url)+ '?session_id={CHECKOUT_SESSION_ID}',
            metadata={
            "user_id": str(request.user.id)
        }
        )

        return redirect(session.url)


    
        