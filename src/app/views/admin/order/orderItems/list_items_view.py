from django.views import View
from django.shortcuts import render, redirect
from app.services.order_service import OrderService

class ListItemView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_service = OrderService()

    def get(self, request, order_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        # Obtener todos los servicios
        items = self.order_service.get_items_by_order_id(order_id)
        for i in items:
            print(i.product)
            print(i.quantity)
        
        # Pasar como "ordenes" para que coincida con el template
        return render(request, "admin/items/list.html", {"items": items})