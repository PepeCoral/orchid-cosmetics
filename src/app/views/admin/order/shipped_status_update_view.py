from django.views import View
from django.shortcuts import render, redirect
from app.services.order_service import OrderService


class ShippedStatusUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_service = OrderService()
    def post(self, request, order_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")
        
        orders = self.order_service.get_all_orders()
        print("Llegue aqui")
        try:
            print(f"Updating order {order_id} to shipped")
            self.order_service.update_order_status_to_shipped(order_id)
            return redirect(f"/admin/orders")
        except Exception as e:
            return render(
                request,
                "admin/orders/list.html",
                {"orders": orders, "error": str(e)}
            )