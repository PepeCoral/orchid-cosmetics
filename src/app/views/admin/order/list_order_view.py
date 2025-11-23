from django.views import View
from django.shortcuts import render, redirect
from app.services.order_service import OrderService

class ListOrderView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_service = OrderService()

    def get(self, request):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        # Obtener todos los servicios
        orders = self.order_service.get_all_orders()
        
        # Pasar como "ordenes" para que coincida con el template
        return render(request, "admin/orders/list.html", {"ordenes": orders})