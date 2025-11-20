from django.views import View
from django.shortcuts import render
from app.services.product_service import ProductService
from app.services.service_service import ServiceService
from app.forms.catalog.search_catalog_form import SearchCatalogForm
from app.models import Category

from django.views import View
from django.shortcuts import render
from app.services.product_service import ProductService
from app.services.service_service import ServiceService
from app.forms.catalog.search_catalog_form import SearchCatalogForm
from app.models import Category

class CatalogView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()
        self.service_service = ServiceService()

    def get(self, request):
        products = self.product_service.get_all_products()
        services = self.service_service.get_all_services()
        categories = Category.objects.all()
        
        # Determinar pestaña activa desde parámetro GET o por defecto
        active_tab = request.GET.get('tab', 'products')

        return render(request, "catalog/catalog.html", {
            "products": products,
            "services": services,
            "categories": categories,
            "form": SearchCatalogForm(),
            "active_tab": active_tab
        })

    def post(self, request):
        search_type = request.POST.get('search_type', 'products')
        
        # Inicializar variables
        products = self.product_service.get_all_products()
        services = self.service_service.get_all_services()
        categories = Category.objects.all()
        
        # Contexto base - la pestaña activa será la del tipo de búsqueda
        context = {
            "products": products,
            "services": services,
            "categories": categories,
            "form": SearchCatalogForm(),
            "active_tab": search_type
        }
        
        if search_type == 'products':
            # Obtener parámetros de productos
            product_name = request.POST.get('product_name', '')
            product_fabricator = request.POST.get('product_fabricator', '')
            product_min_price = request.POST.get('product_min_price', '')
            product_max_price = request.POST.get('product_max_price', '')
            selected_product_categories = request.POST.getlist('product_categories', [])
            
            # Agregar al contexto para mantener valores en el formulario
            context.update({
                'product_name': product_name,
                'product_fabricator': product_fabricator,
                'product_min_price': product_min_price,
                'product_max_price': product_max_price,
                'selected_product_categories': [int(cat) for cat in selected_product_categories if cat],
                'product_filters_active': any([product_name, product_fabricator, product_min_price, product_max_price, selected_product_categories])
            })
            
            # Construir filtros compatibles con ProductRepository
            filters = {}
            if product_name:
                filters['name'] = product_name
            if product_fabricator:
                filters['fabricator'] = product_fabricator
            if product_min_price:
                try:
                    filters['min_price'] = float(product_min_price)
                except ValueError:
                    pass
            if product_max_price:
                try:
                    filters['max_price'] = float(product_max_price)
                except ValueError:
                    pass
            if selected_product_categories:
                filters['categories'] = selected_product_categories
            
            # Aplicar filtros si hay alguno
            if filters:
                try:
                    products = self.product_service.search_products(filters)
                    context['products'] = products
                except Exception as e:
                    context['error'] = f"Error al filtrar productos: {str(e)}"
                
        elif search_type == 'services':
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

        return render(request, "catalog/catalog.html", context)