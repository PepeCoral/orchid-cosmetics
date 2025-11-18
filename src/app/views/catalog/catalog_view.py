from django.views import View
from django.shortcuts import render
from app.services.product_service import ProductService
from app.services.service_service import ServiceService
from app.forms.catalog.search_catalog_form import SearchCatalogForm

class CatalogView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()
        self.service_service = ServiceService()

    def get(self, request):
        form = SearchCatalogForm()
        products = self.product_service.get_all_products()
        services = self.service_service.get_all_services()
        
        return render(request, "catalog/catalog.html", {
            "products": products,
            "services": services,
            "form": form
        })

    def post(self, request):
        form = SearchCatalogForm(request.POST)
        products = self.product_service.get_all_products()
        services = self.service_service.get_all_services()
        
        if form.is_valid():
            # Filtrar productos
            products = self._filter_products(products, form.cleaned_data)
            # Filtrar servicios  
            services = self._filter_services(services, form.cleaned_data)
        
        return render(request, "catalog/catalog.html", {
            "products": products,
            "services": services,
            "form": form
        })
    
    def _filter_products(self, products, filters):
        """Aplicar filtros a productos"""
        queryset = products
        
        if filters.get('name'):
            queryset = queryset.filter(name__icontains=filters['name'])
        
        if filters.get('fabricator'):
            queryset = queryset.filter(fabricator__icontains=filters['fabricator'])
        
        if filters.get('min_price'):
            queryset = queryset.filter(price__gte=filters['min_price'])
        
        if filters.get('max_price'):
            queryset = queryset.filter(price__lte=filters['max_price'])
        
        if filters.get('categories'):
            queryset = queryset.filter(categories__in=filters['categories']).distinct()
        
        return queryset
    
    def _filter_services(self, services, filters):
        """Aplicar filtros a servicios"""
        queryset = services
        
        if filters.get('name'):
            queryset = queryset.filter(name__icontains=filters['name'])
        
        if filters.get('department'):
            queryset = queryset.filter(department__icontains=filters['department'])
        
        if filters.get('min_price'):
            queryset = queryset.filter(price__gte=filters['min_price'])
        
        if filters.get('max_price'):
            queryset = queryset.filter(price__lte=filters['max_price'])
        
        if filters.get('categories'):
            queryset = queryset.filter(categories__in=filters['categories']).distinct()
        
        return queryset