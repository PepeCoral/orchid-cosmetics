from django.views import View
from django.shortcuts import render
from app.services.service_service import ServiceService
from app.forms.catalog.search_catalog_form import SearchCatalogForm
from app.models import Category

class ServiceCatalogView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def get(self, request):
        services = self.service_service.get_all_services()
        categories = Category.objects.all()

        return render(request, "catalog/service_catalog.html", {
            "services": services,
            "categories": categories,
            "form": SearchCatalogForm(),
        })

    def post(self, request):
        # Inicializar variables
        services = self.service_service.get_all_services()
        categories = Category.objects.all()
        
        # Contexto base
        context = {
            "services": services,
            "categories": categories,
            "form": SearchCatalogForm(),
        }
        
        # Obtener parámetros de servicios
        service_name = request.POST.get('service_name', '')
        service_department = request.POST.get('service_department', '')
        service_min_price = request.POST.get('service_min_price', '')
        service_max_price = request.POST.get('service_max_price', '')
        selected_service_categories = request.POST.getlist('service_categories', [])
        
        # Agregar al contexto para mantener valores en el formulario
        context.update({
            'service_name': service_name,
            'service_department': service_department,
            'service_min_price': service_min_price,
            'service_max_price': service_max_price,
            'selected_service_categories': [int(cat) for cat in selected_service_categories if cat],
            'service_filters_active': any([service_name, service_department, service_min_price, service_max_price, selected_service_categories])
        })
        
        # Construir filtros compatibles con ServiceRepository
        filters = {}
        if service_name:
            filters['name'] = service_name
        if service_department:
            filters['department'] = service_department
        if service_min_price:
            try:
                filters['min_price'] = float(service_min_price)
            except ValueError:
                pass
        if service_max_price:
            try:
                filters['max_price'] = float(service_max_price)
            except ValueError:
                pass
        if selected_service_categories:
            filters['categories'] = selected_service_categories
        
        # Aplicar filtros si hay alguno
        if filters:
            try:
                services = self.service_service.search_services(filters)
                context['services'] = services
            except Exception as e:
                context['error'] = f"Error al filtrar servicios: {str(e)}"

        return render(request, "catalog/service_catalog.html", context)