from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Q
from app import models
from app.models import Service, Category
from app.repositories.order_repository import OrderRepository
from app.repositories import product_repository as ProductRepository
from app.repositories.product_quantity_repository import ProductQuantityRepository
from app.repositories.service_quantity_repository import ServiceQuantityRepository
from app.models import ServiceQuantity, ProductQuantity, Order, Product, Service, User


class OrderService():
    
    def __init__(self):
        self.order_repository = OrderRepository()

    def create_current_order(self,user) -> Order:
        pass
    
    @staticmethod
    def create_order(order_data):
        """
        Crea un nuevo servicio
        """
        qs = QuantityService()

        user = User.objects.get(id=1)
        order = Order(
            user=user,
            address=order_data['address'],
            payMethod=order_data['payMethod'],
            delivery_method=order_data['delivery_method']
            )
        order.save()
        qs.assign_quantities_to_order(order)
        return order
            
    @staticmethod
    def get_all_orders():
        return Order.objects.all()
class QuantityService():
    def __init__(self):
        self.prod_quantity_repo = ProductQuantityRepository()
        self.serv_quantity_repo = ServiceQuantityRepository()

    def create_service_quantity(self, service, quantity=1):
        
        serviceQ = ServiceQuantity(
            quantity=quantity,
            service=service
        )
        serviceQ.save()
        return serviceQ
    
    def create_product_quantity(self,product, quantity=1):
        productQ = ProductQuantity(
            quantity=quantity,
            product=product
        )
        productQ.save()
        return productQ
        
    
    def get_all_services_quantities(self):
        servicesQ = ServiceQuantity.objects.all()
        dicc = {}
        for service in servicesQ:
            totalQuant=service.quantity
            if not dicc.get(service.service):
                dicc[service.service]=totalQuant
            else:
                dicc[service.service]+=totalQuant
        
        return dicc

    def get_all_product_quantities(self):
        productsQ = ProductQuantity.objects.all()   
        dicc = {}
        for product in productsQ:
            totalQuant=product.quantity
            if not dicc.get(product.product):
                dicc[product.product]=totalQuant
            else:
                dicc[product.product]+=totalQuant
            
        return dicc

    def assign_quantities_to_order(self, order):
    # Productos sin orden asignada
        product_quantities = ProductQuantity.objects.filter(order__isnull=True)
        for pq in product_quantities:
            pq.order = order
            pq.save()

    # Servicios sin orden asignada
        service_quantities = ServiceQuantity.objects.filter(order__isnull=True)
        for sq in service_quantities:
            sq.order = order
            sq.save()
        