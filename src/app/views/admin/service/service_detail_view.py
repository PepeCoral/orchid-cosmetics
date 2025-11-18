# app/views/service/service_detail_view.py
from django.views import View
from django.shortcuts import render
from app.services.service_service import ServiceService

class ServiceDetailView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def get(self, request, service_id):
        service = self.service_service.get_service_by_id(service_id)
        categories = service.categories.all()
        return render(request, "service/detail.html", {
            "service": service,
            "categories": categories
        })