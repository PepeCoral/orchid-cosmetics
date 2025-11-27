from django.views import View
from django.shortcuts import render, redirect
from app.services.order_service import OrderService

class ListItemView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_service = OrderService()

    def get(self, request, order_id):
    
        products_items = self.order_service.get_products_by_order_id(order_id)
        services_items = self.order_service.get_services_by_order_id(order_id)
        order = self.order_service.get_order_by_id(order_id)
        coste = self.order_service.get_total_cost_by_order_id(order_id)
        
        context = {"products_items": products_items, "services_items": services_items, "order": order, "coste": coste}

        return render(request, "items/list.html", context)