from django.views import View
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
import stripe
from django.conf import settings
from app.services.order_service import OrderService

stripe.api_key = settings.STRIPE_SECRET_KEY

@method_decorator(csrf_exempt,name="dispatch")
class StripeWebhookView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_service = OrderService()

    def post(self,request: HttpRequest):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)
        
        if event["type"] == "checkout.session.completed":
            order = self.order_service.create_current_order(request.user)
        
        return HttpResponse(status = 200)