from django.views import View
from django.shortcuts import render, redirect
from app.services.order_service import OrderService
from app.forms.orders.anonymous_search_order_form import AnonymusSearchOrderForm

class IdentifierOrderView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_service = OrderService()

    def get(self, request, identifier):
        try:
            order = self.order_service.get_order_by_identifier_2(identifier)
            products_items = self.order_service.get_products_by_order_id(order.id)
            services_items = self.order_service.get_services_by_order_id(order.id)
            coste = self.order_service.get_total_cost_by_order_id(order.id)

            context = {"products_items": products_items, "services_items": services_items, "order": order, "coste": coste}
            return render(request, "items/list.html", context)
        except Exception as e:
            return redirect("/")
