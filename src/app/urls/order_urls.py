from django.urls import path
from app import views

urlpatterns = [
    path('orders/create/', views.create_order, name="create_order"),
    path('orders/', views.get_all_orders, name="get_all_orders"),
]
