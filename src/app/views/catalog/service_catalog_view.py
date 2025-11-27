from django.views import View
from django.shortcuts import render
from app.forms.service.buy_service_form import BuyServiceForm
from app.services.service_service import ServiceService
from app.services.service_service import ServiceService
from app.forms.catalog.search_service_catalog_form import SearchServiceCatalogForm



class ServiceCatalogView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def get(self, request):
        try:
          form = SearchServiceCatalogForm()
          rent_form = BuyServiceForm()
          services = self.service_service.get_all_services()

          return render(request, "catalog/service_catalog.html", {
              "services": services,
              "form": form,
              "rent_form":rent_form
          })
        except Exception as e:
          print(e)

    def post(self, request):
        form = SearchServiceCatalogForm(request.POST)
        rent_form = BuyServiceForm()

        if form.is_valid():
            services = self.service_service.search_services(form.cleaned_data)

        return render(request, "catalog/service_catalog.html", {
            "services": services,
            "form": form,
            "rent_form":rent_form
        })
