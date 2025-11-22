from django.views import View
from django.shortcuts import render,redirect
from app.forms.checkout.checkout_form import CheckoutForm
from app.services.order_service import OrderService
from app.services.cart_item_service import CartService
from app.models.product import Product
from app.models.service import Service
from app.models.order import PaymentMethodOptions
from django.http import HttpRequest

class CheckoutView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_service = CartService()
        self.order_service = OrderService()

    def get(self, request):
        cart_items = self.cart_service.get_cart_items(request)
        form = CheckoutForm()
        total = self.cart_service.get_total(request)

        products = []
        services = []
        for item in cart_items:
            if isinstance(item.item, Product):
                products.append(item)
                if item.quantity> item.item.stock:
                    error = f"El producto {item.item.name} tiene stock {item.item.stock} y está intentando comprar {item.quantity}"
                    return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total, "error": error})
            elif isinstance(item.item, Service):
                services.append(item)


        

        return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total})

    

    def post(self, request: HttpRequest):

        cart_items = self.cart_service.get_cart_items(request)
        form = CheckoutForm(request.POST)
        total = self.cart_service.get_total(request)
        
        products = []
        services = []
        for item in cart_items:
            if isinstance(item.item, Product):
                products.append(item)
                if item.quantity> item.item.stock:
                    error = f"El producto {item.item.name} tiene stock {item.item.stock} y está intentando comprar {item.quantity}"
                    return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total, "error": error})
            elif isinstance(item.item, Service):
                services.append(item)



        if not form.is_valid():
            return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total})
        form_cleaned_data = form.cleaned_data
        pay_method = form_cleaned_data.get("pay_method")
        if pay_method is PaymentMethodOptions.PAYMENT_GATEWAY:
            try:
                session_url = self.order_service.create_stripe_session(request=request,form=form)
                return redirect(session_url)
            except Exception as e:
                return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total, "error": e})
        

        user = request.user
        user_id = None
        session_key = None
        if user.is_anonymous:
            if not request.session.session_key:
              request.session.create()
            session_key = request.session.session_key
        else:
            user_id = user.id

        order = self.order_service.create_current_order(user_id=user_id,session_key=session_key,
                                                address=form_cleaned_data.get("address"), 
                                                delivery_method=form_cleaned_data.get("delivery_method"), 
                                                pay_method=form_cleaned_data.get("pay_method") )

        total = self.order_service.get_total_cost_by_order_id(order.id)

        return render(request, "checkout/success_cod.html", {"total": total})