from django.views import View
from django.shortcuts import render, redirect
from app.services.product_service import ProductService

from app.forms.catalog.search_catalog_form import SearchCatalogForm
class CatalogView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def get(self, request):
        form = SearchCatalogForm()
        products = self.product_service.get_all_products()
        return render(request, "catalog.html", {"form": form, "products": products})

    def post(self, request):

        form = SearchCatalogForm(request.POST)

        if not form.is_valid():
            return render(request, "catalog.html", {"form": form})

        try:
            products = self.product_service.search(form.cleaned_data)
            return render(request, "catalog.html", {"form": form, "products": products})
        except Exception as e:
            products = self.product_service.get_all_products()
            return render(
                request,
                "catalog.html",
                {"form": form, "products": products,  "error": str(e)}
            )
