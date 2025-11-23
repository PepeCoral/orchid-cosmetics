from django.views import View
from django.shortcuts import render, redirect
from app.services.order_service import OrderService
from app.forms.orders.anonymous_search_order_form import AnonymusSearchOrderForm

class AnonymousSearchOrderView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_service = OrderService()

    def get(self, request):
        # Obtener todos los servicios
        form = AnonymusSearchOrderForm()
        
        # Pasar como "ordenes" para que coincida con el template
        return render(request, "orders/anonymous_list.html", {"form": form})
    
    def post(self, request):
        form = AnonymusSearchOrderForm(request.POST)

        if not form.is_valid():
            return render(request, "orders/anonymous_list.html", {"form": form})

        try:
            order = self.order_service.get_order_by_identifier(form.cleaned_data)
            products_items = self.order_service.get_products_by_order_id(order.id)
            services_items = self.order_service.get_services_by_order_id(order.id)
            coste = self.order_service.get_total_cost_by_order_id(order.id)

            context = {"products_items": products_items, "services_items": services_items, "order": order, "coste": coste}
            return render(request, "items/list.html", context)
        except Exception as e:
            return render(
                request,
                "orders/anonymous_list.html",
                {"form": form, "error": str(e)}
            )