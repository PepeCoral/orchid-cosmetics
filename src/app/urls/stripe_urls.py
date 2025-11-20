from django.urls import path
from app.views.stripe.stripe_webhook_view import StripeWebhookView
from app.views.stripe.create_session_stripe_view import CreateSessionStripeView
from app.views.stripe.success_checkout_view import SuccessCheckoutView
from app.views.stripe.cancel_checkout_view import CancelCheckoutView

urlpatterns = [
    path("stripe/webhook/", StripeWebhookView.as_view(), name="stripe_webhook"),
    path("checkout/", CreateSessionStripeView.as_view(), name="checkout"),
    path("checkout/success/", SuccessCheckoutView.as_view(), name="checkout_success"),
    path("checkout/cancel/", CancelCheckoutView.as_view(), name="checkout_cancel"), 

]