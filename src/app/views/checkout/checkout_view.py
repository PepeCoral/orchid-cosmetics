from django.views import View
from django.shortcuts import render,redirect
from app.forms.checkout.checkout_form import CheckoutForm
from app.services.order_service import OrderService
from app.services.user_service import UserService
from app.services.cart_item_service import CartService
from app.models.product import Product
from app.models.service import Service

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

    

    def post(self, request):

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


        try:
            session_url = self.order_service.create_stripe_session(request=request,form=form)
            return redirect(session_url)
        except Exception as e:
            return render(request, "checkout/checkout.html", {"form": form, "products": products, "services": services, "total": total, "error": e})
