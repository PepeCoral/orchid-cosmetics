from django.views import View
from django.shortcuts import render
from app.forms.product.buy_product_form import BuyProductForm
from app.services.product_service import ProductService
from app.services.service_service import ServiceService
from app.forms.catalog.search_product_catalog_form import SearchProductCatalogForm



class ProductCatalogView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def get(self, request):
        try:
          form = SearchProductCatalogForm()
          buy_form = BuyProductForm()
          products = self.product_service.get_all_products()

          return render(request, "catalog/product_catalog.html", {
              "products": products,
              "form": form,
              "buy_form": buy_form
          })
        except Exception as e:
          print(e)

    def post(self, request):
        form = SearchProductCatalogForm(request.POST)
        buy_form = BuyProductForm()

        if form.is_valid():
            products = self.product_service.search_products(form.cleaned_data)

        return render(request, "catalog/product_catalog.html", {
            "products": products,
            "form": form,
            "buy_form": buy_form
        })
