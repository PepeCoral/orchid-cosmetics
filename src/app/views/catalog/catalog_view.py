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

            products = self._filter_products(form.cleaned_data)
            services = self._filter_services(form.cleaned_data)
        
        return render(request, "catalog/catalog.html", {
            "products": products,
            "services": services,
            "form": form
        })
    
    def _filter_products(self, filters):

        return self.product_service.search(filters)
    
    def _filter_services(self, filters):

        return self.service_service.search_services(filters)