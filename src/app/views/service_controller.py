from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json
from app.services.service_service import ServiceService
from app.forms.service_form import ServiceForm
from django.shortcuts import redirect, render

@csrf_exempt
@require_http_methods(["POST", "GET"])
def create_service(request):
    """Crear un nuevo servicio"""

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            ServiceService.create_service(request,form.cleaned_data)
            return redirect("/services", "service.html")
        else:
            return render(request, "createservice.html", {"form": form})
    
    form = ServiceForm()
    return render(request,"createservice.html", context={"form":form})

@require_http_methods(["GET"])
def get_service(request, service_id):
    """Obtener un servicio por ID"""
    service = ServiceService.get_service_by_id(service_id)
    return render(request, "detailservices.html", {"servicio":service})

@require_http_methods(["GET"])
def list_services(request):
    """Listar todos los servicios"""
    services = ServiceService.get_all_services()
    return render(request, "services.html", {"servicios": services})
    
