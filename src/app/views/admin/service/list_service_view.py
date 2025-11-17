from django.views import View
from django.shortcuts import render, redirect
from app.services.service_service import ServiceService
from django.http import HttpRequest

class ListServiceView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def get(self,request: HttpRequest):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")
        
        services = self.service_service.get_all_services()

        return render(request, "admin/services/list.html", {"services": services})
