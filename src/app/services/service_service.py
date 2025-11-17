from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Q
from app import models
from app.models import Service, Category
from app.repositories.service_repository import ServiceRepository


class ServiceService():
    
    def __init__(self):
        self.service_repository = ServiceRepository()

    def create_service(self,request,service_data):
       
        if(service_data["price"] < 0):
            raise ValidationError("Price cannot be negative")
        if(service_data["duration_minutes"] < 0):
            raise ValidationError("Duration cannot be negative")


        files = request.FILES
        service_data["image_url"] = files.get("image_url")
        categories = service_data.pop("categories")
        service = self.service_repository.create(**service_data)
        service.categories.set(categories)

        return service
    
    @staticmethod
    def get_service_by_id(service_id):
        """
        Obtiene un servicio por su ID
        """
        try:
            return Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            raise ValidationError("Servicio no encontrado")
    
    @staticmethod
    def get_all_services():
        """
        Obtiene todos los servicios con sus categorías
        """
        return Service.objects.all().prefetch_related('categories')
    