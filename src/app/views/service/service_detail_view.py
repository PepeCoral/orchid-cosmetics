from django.views import View
from django.shortcuts import render, redirect
from app.services.service_service import ServiceService
from app.services.cart_item_service import CartService
from app.forms.service.buy_service_form import BuyServiceForm

class ServiceDetailView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()
        self.cart_service = CartService()

    def get(self, request, service_id):
        try:
          service = self.service_service.get_service_by_id(service_id)
          categories = service.categories.all()

          form = BuyServiceForm()

          return render(request, "service/detail.html", {
              "form": form,
              "service": service,
              "categories": categories
          })
        except Exception as e:
            print(e)

    def post(self, request, service_id):
        service = self.service_service.get_service_by_id(service_id)
        categories = service.categories.all()

        form = BuyServiceForm(request.POST)

        if not form.is_valid():
            return render(request, "service/detail.html", {
                "form": form,
                "service": service,
                "categories": categories
            })

        try:

            quantity = form.cleaned_data['quantity']
            self.cart_service.add_item(request, service, quantity)

            return redirect("/cart")
        except Exception as e:
            return render(
                request,
                "service/detail.html",
                {
                    "form": form,
                    "error": str(e),
                    "service": service,
                    "categories": categories
                }
            )
