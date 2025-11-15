from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Q
from app import models
from app.models import Service, Category
from app.repositories import product_repository as ProductRepository
from app.repositories.product_quantity_repository import ProductQuantityRepository
from app.repositories.service_quantity_repository import ServiceQuantityRepository
from app.models import ServiceQuantity, ProductQuantity, Order, Product, Service


class OrderService():
    
    
    @staticmethod
    def create_category(category_data):
        """
        Crea un nuevo servicio
        """
        category = Category(name=category_data['name'])
        category.save()
        return category
            
    
    @staticmethod
    def get_category_by_id(category_id):
        """
        Obtiene un servicio por su ID
        """
        return Category.objects.get(id=category_id)
    
    @staticmethod
    def get_category_by_name(name):
        return Category.objects.get(name=name)
    
    @staticmethod
    def get_all_categories():
        """
        Obtiene todos los servicios con sus categorías
        """
        return Category.objects.all()
    
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
        