from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json
from app.services.product_service import ProductService
from app.forms.product_form import ProductForm
from django.shortcuts import redirect, render

product_serv = ProductService()

@csrf_exempt
@require_http_methods(["POST", "GET"])
def create_product(request):
    """Crear un nuevo producto"""

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_serv.create_product(request,form.cleaned_data)
            return redirect("/products", "product/list.html")
        else:
            return render(request, "product/create.html", {"form": form})
    
    form = ProductForm()
    return render(request,"product/create.html", context={"form":form})

@require_http_methods(["GET"])
def get_product(request, product_id):
    """Obtener un servicio por ID"""
    product = product_serv.get_product_by_id(product_id)
    categories = product.categories.all()
    return render(request, "product/detail.html", {"producto":product, "categories":categories})

@require_http_methods(["GET"])
def list_products(request):
    """Listar todos los servicios"""
    product = product_serv.get_all_products()
    return render(request, "product/list.html", {"productos": product})