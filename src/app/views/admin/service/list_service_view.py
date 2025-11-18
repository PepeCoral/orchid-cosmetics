from django.views import View
from django.shortcuts import render, redirect
from app.services.service_service import ServiceService

class ListServiceView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def get(self, request):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        # Obtener todos los servicios
        services = self.service_service.get_all_services()
        
        # Pasar como "servicios" para que coincida con el template
        return render(request, "admin/services/list.html", {"servicios": services})
