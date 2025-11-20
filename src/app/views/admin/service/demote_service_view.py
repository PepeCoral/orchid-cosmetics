from django.views import View
from django.shortcuts import render, redirect
from app.services.service_service import ServiceService


class DemoteServiceView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def post(self, request, service_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")
        
        services = self.service_service.get_all_services()
        try:
            self.service_service.demote_service(service_id)
            return redirect(f"/admin/cosmeticservices")
        except Exception as e:
            return render(
                request,
                "admin/services/list.html",
                {"servicios": services, "error": str(e)}
            )