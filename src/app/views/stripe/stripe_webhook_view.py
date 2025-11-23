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
        payload = request.body.decode("utf-8")
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.SignatureVerificationError:
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            session = event['data']['object']
            metadata =session['metadata']
            user_id = metadata.get('user_id',None)
            session_key = metadata.get('session_key',None)
            address = metadata.get('address', None)
            delivery_method = metadata.get('delivery_method', None)
            pay_method = metadata.get('pay_method', None)
            email = metadata.get('email', None)

            order = self.order_service.create_current_order(user_id=user_id,
                                                            session_key=session_key, address=address,
                                                            delivery_method=delivery_method,pay_method=pay_method, email=email)

        return HttpResponse(status = 200)
