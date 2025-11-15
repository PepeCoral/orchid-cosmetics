from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Q
from app import models
from app.models import Service, Category


class ServiceService():
    
    
    @staticmethod
    def create_service(request,service_data):
        """
        Crea un nuevo servicio
        """
        try:

            files = request.FILES

            service = Service(
                name=service_data['name'],
                description=service_data['description'],
                price=service_data['price'],
                duration_minutes=service_data['duration_minutes'],
                department=service_data['department'],
                image_url=files.get('image_url')
            )
            
            service.save()
            if 'categories' in service_data:
                service.categories.set(service_data['categories'])
            return service
            
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Error al crear el servicio: {str(e)}")
    
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
    