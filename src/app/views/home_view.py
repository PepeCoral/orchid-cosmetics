from django.views import View
from django.shortcuts import render
from app.services.product_service import ProductService
from app.services.service_service import ServiceService

class HomeView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()
        self.service_service = ServiceService()

    def get(self, request):
        products = self.product_service.get_all_products()
        services = self.service_service.get_all_services()

        context = {
            "products": products,   
            "services": services
        }
        return render(request, "home.html", context)
