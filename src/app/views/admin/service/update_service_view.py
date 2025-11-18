from django.views import View
from django.shortcuts import render, redirect
from app.forms.service.update_service_form import UpdateServiceForm
from app.services.service_service import ServiceService

class UpdateServiceView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def get(self, request, service_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        service = self.service_service.get_service_by_id(service_id)
        form = UpdateServiceForm(instance=service)

        return render(request, "admin/services/update.html", {"form": form})

    def post(self, request, service_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        service = self.service_service.get_service_by_id(service_id)
        form = UpdateServiceForm(request.POST, request.FILES, instance=service)

        if not form.is_valid():
            return render(request, "admin/services/update.html", {"form": form})

        try:
            self.service_service.update_service(service_id, form.cleaned_data, request)
            return redirect("admin/cosmeticservices")
        except Exception as e:
            return render(
                request,
                "admin/services/update.html",
                {"form": form, "error": str(e)}
            )