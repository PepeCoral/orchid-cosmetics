from decimal import Decimal
from django.core.exceptions import ValidationError
from django.http import Http404
from app.models import Service, Category
from app.repositories.service_repository import ServiceRepository

class ServiceService():

    def __init__(self):
        self.service_repository = ServiceRepository()

    def create_service(self, request, service_data):
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

    def get_promoted_services(self):
        return self.service_repository.get_all_promoted_services()

    def promote_service(self,service_id):
        service = self.service_repository.get_by_id(service_id)
        if not service:
            raise ValidationError("Servicio no encontrado.")
        print("hola")
        updated_service = self.service_repository.update(id=service_id,isPromoted=True)
        return updated_service

    def demote_service(self,service_id):
        service = self.service_repository.get_by_id(service_id)
        if not service:
            raise ValidationError("Servicio no encontrado.")
        updated_service = self.service_repository.update(id=service_id,isPromoted=False)
        return updated_service
    
    def get_service_by_id(self, service_id):
        """
        Obtiene un servicio por su ID
        """
        try:
            return Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            raise ValidationError("Servicio no encontrado")

    def get_all_services(self):
        """
        Obtiene todos los servicios con sus categorías
        """
        return Service.objects.all().prefetch_related('categories')

    def update_service(self, service_id, service_data, request):
        """
        Actualiza un servicio existente
        """
        service = self.service_repository.get_by_id(service_id)
        if not service:
            raise ValidationError("Servicio no encontrado.")

        # Validaciones
        if "price" in service_data and service_data["price"] < 0:
            raise ValidationError("El precio no puede ser negativo")
        if "duration_minutes" in service_data and service_data["duration_minutes"] < 0:
            raise ValidationError("La duración no puede ser negativa")

        # Manejar imagen si se envió
        files = request.FILES
        if 'image_url' in files:
            service_data["image_url"] = files.get("image_url")

        # Manejar categorías si se enviaron
        categories = None
        if "categories" in service_data:
            categories = service_data.pop("categories")

        # Actualizar servicio
        updated_service = self.service_repository.update(service_id, **service_data)

        # Actualizar categorías si se proporcionaron
        if categories is not None:
            updated_service.categories.set(categories)

        return updated_service

    def delete_service(self, service_id):
        service = self.service_repository.get_by_id(service_id)
        if not service:
            raise ValidationError("Servicio no encontrado.")

        return self.service_repository.delete(service_id)

    def search_services(self, filters):
        return self.service_repository.search(filters)
