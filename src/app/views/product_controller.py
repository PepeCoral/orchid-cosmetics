from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json
from app.services.order_service import QuantityService
from app.services.product_service import ProductService
from app.forms.product.create_product_form import CreateProductForm
from django.shortcuts import redirect, render

product_serv = ProductService()

@csrf_exempt
@require_http_methods(["POST", "GET"])
def create_product(request):
    """Crear un nuevo producto"""

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_serv.create_product(request,form.cleaned_data)
            return redirect("/products", "product/list.html")
        else:
            return render(request, "product/create.html", {"form": form})

    form = CreateProductForm()
    return render(request,"product/create.html", context={"form":form})


@csrf_exempt
@require_http_methods(["GET","POST"])
def get_product(request, product_id):
    """Obtener un servicio por ID"""
    product = product_serv.get_product_by_id(product_id)
    categories = product.categories.all()
    if request.method=="POST":
        qs = QuantityService()
        qs.create_product_quantity(product)
    return render(request, "product/detail.html", {"producto":product, "categories":categories})
