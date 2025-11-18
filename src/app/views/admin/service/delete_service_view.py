from django.views import View
from django.shortcuts import render, redirect
from app.forms.service.delete_service_form import DeleteServiceForm
from app.services.service_service import ServiceService

class DeleteServiceView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def get(self, request, service_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        service = self.service_service.get_service_by_id(service_id)
        form = DeleteServiceForm()

        return render(request, "admin/services/delete.html", {"form": form, "service": service})

    def post(self, request, service_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        form = DeleteServiceForm(request.POST)

        if not form.is_valid():
            service = self.service_service.get_service_by_id(service_id)
            return render(request, "admin/services/delete.html", {"form": form, "service": service})

        try:
            self.service_service.delete_service(service_id)
            return redirect("admin/cosmeticservices")
        except Exception as e:
            service = self.service_service.get_service_by_id(service_id)
            return render(
                request,
                "admin/services/delete.html",
                {"form": form, "service": service, "error": str(e)}
            )