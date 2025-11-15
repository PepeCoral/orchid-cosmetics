from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json
from app.services.category_service import CategoryService
from app.forms.category_form import CategoryForm
from django.shortcuts import redirect, render

@csrf_exempt
@require_http_methods(["POST", "GET"])
def create_category(request):
    """Crear un nuevo servicio"""

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            CategoryService.create_category(form.cleaned_data)
            return redirect("/categories", "categories/list.html")
        else:
            return render(request, "categories/create.html", {"form": form})
    
    form = CategoryForm()
    return render(request,"categories/create.html", context={"form":form})

@require_http_methods(["GET"])
def get_category(request, category_id):
    """Obtener un servicio por ID"""
    category = CategoryService.get_category_by_id(category_id)
    return render(request, "categories/detail.html", {"categoria":category})

@require_http_methods(["GET"])
def list_categories(request):
    """Listar todos los servicios"""
    categories = CategoryService.get_all_categories()
    return render(request, "categories/list.html", {"categorias": categories})
    
