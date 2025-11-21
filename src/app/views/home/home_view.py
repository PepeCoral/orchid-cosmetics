from django.views import View
from django.shortcuts import render
from app.services.product_service import ProductService
from app.services.service_service import ServiceService
from app.forms.catalog.search_product_catalog_form import SearchProductCatalogForm
from app.forms.catalog.search_service_catalog_form import SearchServiceCatalogForm

class HomeView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()
        self.service_service = ServiceService()

    def get(self, request):
        products = self.product_service.get_promoted_products()
        services = self.service_service.get_promoted_services()

        form = SearchProductCatalogForm()
        formS = SearchServiceCatalogForm()
        context = {
            "products": products,   
            "services": services,
            "form":form,
            "formS":formS
        }
        return render(request, "home.html", context)
    
