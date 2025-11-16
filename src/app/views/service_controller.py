from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json
from app.services.order_service import QuantityService
from app.services.category_service import CategoryService
from app.services.service_service import ServiceService
from app.forms.service_form import ServiceForm
from django.shortcuts import redirect, render

service = ServiceService()

@csrf_exempt
@require_http_methods(["POST", "GET"])
def create_service(request):
    """Crear un nuevo servicio"""

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service.create_service(request,form.cleaned_data)
            return redirect("/services", "service.html")
        else:
            return render(request, "services/create.html", {"form": form})
    
    form = ServiceForm()
    return render(request,"services/create.html", context={"form":form})

@csrf_exempt
@require_http_methods(["GET"])
def get_service(request, service_id):
    """Obtener un servicio por ID"""
    foundService = service.get_service_by_id(service_id)
    return render(request, "services/detail.html", {"servicio":foundService})

@require_http_methods(["GET"])
def list_services(request):
    """Listar todos los servicios"""
    services = service.get_all_services()
    return render(request, "services/list.html", {"servicios": services})
    
