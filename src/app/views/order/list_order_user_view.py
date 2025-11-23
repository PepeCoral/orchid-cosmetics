from django.views import View
from django.shortcuts import render, redirect
from app.services.order_service import OrderService

class ListOrderUserView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_service = OrderService()

    def get(self, request):
        if request.user.is_anonymous:
            return redirect("/")

        # Obtener todos los servicios
        orders = self.order_service.get_orders_by_user_id(request.user.id)
        
        # Pasar como "ordenes" para que coincida con el template
        return render(request, "orders/list.html", {"ordenes": orders})