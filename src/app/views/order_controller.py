from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json
from app.services.order_service import QuantityService
from app.services.product_service import ProductService
from app.services.service_service import ServiceService
from app.services.order_service import OrderService
from app.forms.order_form import OrderForm
from django.shortcuts import redirect, render

product_ser = ProductService()
service_ser = ServiceService()
order_ser = OrderService()

@require_http_methods(["GET"])
def get_all_quantity(request):
    qs = QuantityService()

    servicesQ = qs.get_all_services_quantities()
    productsQ = qs.get_all_product_quantities()
    
    print(set(productsQ.keys()))
    servicesQ = list(servicesQ.items())
    productsQ = list(productsQ.items())
    return render(request, "orders/shopping.html",{"servicesQ":servicesQ,
                                                    "productsQ":productsQ
                                                    })

@csrf_exempt
@require_http_methods(["GET","POST"])
def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order_ser.create_order(form.cleaned_data)
            return redirect("/","base.html")
        else:
            return render(request, "orders/create.html", {"form":form})
    
    form = OrderForm()
    return render(request, "orders/create.html", {"form":form})

@require_http_methods(["GET"])
def get_all_orders(request):
    orders = order_ser.get_all_orders()
    return render(request, "orders/list.html",{"orders":orders})
