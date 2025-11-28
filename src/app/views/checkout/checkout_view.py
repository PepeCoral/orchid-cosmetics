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

    def get(self, request: HttpRequest):
        try:
          cart_items = self.cart_service.get_cart_items(request)
          user = request.user
          initial_data = {}

          if hasattr(user,"pay_method") and user.pay_method:
              initial_data["pay_method"] =user.pay_method

          if hasattr(user,"address") and user.address:
              initial_data["address"] =user.address

          if hasattr(user,"email") and user.email:
              initial_data["email"] =user.email



          form = CheckoutForm(initial=initial_data)
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
          shipping_cost = OrderService.calculate_shipping_costs(products)
          total = float(total) + shipping_cost

          total = round(total,2)



          return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total, "shipping": shipping_cost})
        except Exception as e:
          import traceback
          print("Error:", e)
          traceback.print_exc()


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
                    return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total, "error": error, "shipping": shipping_cost})
            elif isinstance(item.item, Service):
                services.append(item)
        shipping_cost = OrderService.calculate_shipping_costs(products)
        total = float(total) + shipping_cost
        total = round(total,2)


        if not form.is_valid():
            return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total, "shipping": shipping_cost})
        form_cleaned_data = form.cleaned_data
        pay_method = form_cleaned_data.get("pay_method")
        if pay_method == PaymentMethodOptions.PAYMENT_GATEWAY.value:

            try:
                session_url = self.order_service.create_stripe_session(request=request,form=form)
                return redirect(session_url)
            except Exception as e:
                return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total, "error": e, "shipping": shipping_cost})


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
                                                pay_method=form_cleaned_data.get("pay_method"), email=form_cleaned_data.get("email"), request=request )

        total = self.order_service.get_total_cost_by_order_id(order.id)
        total = round(total,2)


        return render(request, "checkout/success_cod.html", {"total": total, "identifier": order.identifier})
