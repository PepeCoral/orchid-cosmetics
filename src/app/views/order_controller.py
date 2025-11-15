from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json
from app.services.order_service import QuantityService
from app.services.product_service import ProductService
from app.services.service_service import ServiceService
from app.forms.product_form import ProductForm
from django.shortcuts import redirect, render

product_ser = ProductService()
service_ser = ServiceService()

@require_http_methods(["GET"])
def get_all_quantity(request):
    qs = QuantityService()

    servicesQ = qs.get_all_services_quantities()
    productsQ = qs.get_all_product_quantities()
    
    print(productsQ)
    for value in productsQ:
        print(value, productsQ[value])
    servicesQ = list(servicesQ.items())
    productsQ = list(productsQ.items())
    return render(request, "orders/shopping.html",{"servicesQ":servicesQ,
                                                    "productsQ":productsQ
                                                    })


