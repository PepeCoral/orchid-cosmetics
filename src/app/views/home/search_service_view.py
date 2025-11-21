from django.views import View
from django.shortcuts import render
from app.services.service_service import ServiceService
from app.forms.catalog.search_service_catalog_form import SearchServiceCatalogForm



class SearchServiceView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def post(self, request):
        form = SearchServiceCatalogForm(request.POST)

        if form.is_valid():
            services = self.service_service.search_services(form.cleaned_data)

        return render(request, "catalog/service_catalog.html", {
            "services": services,
            "form": form
        })
