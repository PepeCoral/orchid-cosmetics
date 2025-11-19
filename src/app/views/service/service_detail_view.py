from django.views import View
from django.shortcuts import render, redirect
from app.services.service_service import ServiceService
from app.forms.service.buy_service_form import BuyServiceForm

class ServiceDetailViewUser(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def get(self, request, service_id):
        service = self.service_service.get_service_by_id(service_id)
        categories = service.categories.all()
        
        form = BuyServiceForm()
        
        return render(request, "service/detail.html", {  # ← SIN "app/"
            "form": form, 
            "service": service,
            "categories": categories
        })

    def post(self, request, service_id):
        if request.user.is_anonymous:
            return redirect("/login")

        service = self.service_service.get_service_by_id(service_id)
        categories = service.categories.all()
        
        form = BuyServiceForm(request.POST)

        if not form.is_valid():
            return render(request, "service/detail.html", {  # ← SIN "app/"
                "form": form, 
                "service": service,
                "categories": categories
            })

        try:
            quantity = form.cleaned_data['quantity']
            return redirect("/cash")
        except Exception as e:
            return render(
                request,
                "service/detail.html",  # ← SIN "app/"
                {
                    "form": form, 
                    "error": str(e), 
                    "service": service,
                    "categories": categories
                }
            )
    