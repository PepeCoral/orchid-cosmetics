from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app.services.service_service import ServiceService

class ShowServiceView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def get(self, request: HttpRequest, service_id: int):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        service = self.service_service.get_service_by_id(service_id)
        categories = service.categories.all()
        return render(request, "admin/services/detail.html", {"service": service, "categories": categories})