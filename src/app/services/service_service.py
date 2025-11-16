from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Q
from app import models
from app.models import Service, Category
from app.repositories.service_repository import ServiceRepository

class ServiceService():

    def __init__(self):
        self.repository = ServiceRepository()

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
                image_url=files.get('image')
            )
            service.save()
            if 'categories' in service_data:
                service.categories.set(service_data['categories'])

            return service
            
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Error al crear el servicio: {str(e)}")
    
    def get_service_by_id(self,service_id:int):
    
        return self.repository.get_by_id(service_id)
    
    def get_all_services(self):
        return self.repository.get_all()
    
    def get_services_by_price_range(self,min_price: float, max_price: float):
    
        return self.repository.get_services_between_prices(min_price,max_price)
    
    def get_services_by_category_name(self,name:str):
        return self.repository.get_services_by_category_name(name)
    
    def get_services_by_category_id(self, id:int):
        return self.repository.get_services_by_category_id(id)
    
    def get_services_by_categories_names(self, categories_names_list:list[str]):
        return self.repository.get_services_by_categories_names(categories_names_list)
    
    def get_services_by_name(self, service_name:str):
        return self.repository.get_services_by_name(service_name)

    @staticmethod
    def get_services_by_category(category_id):
        """
        Obtiene servicios por categoría
        """
        try:
            category = Category.objects.get(id=category_id)
            return Service.objects.filter(category=category).prefetch_related('categories')
        except Category.DoesNotExist:
            raise ValidationError("Categoría no encontrada")
    
    @staticmethod
    def get_services_by_department(department):
        """
        Obtiene servicios por departamento (case-insensitive)
        """
        return Service.objects.filter(department__iexact=department).prefetch_related('categories')
    
    @staticmethod
    def update_service(service_id, update_data):
        """
        Actualiza un servicio existente
        """
        try:
            service = Service.objects.get(id=service_id)
            
            # Verificar nombre duplicado
            if 'name' in update_data:
                if Service.objects.filter(name=update_data['name']).exclude(id=service_id).exists():
                    raise ValidationError("Ya existe un servicio con este nombre")
                service.name = update_data['name']
            
            # Actualizar otros campos
            if 'description' in update_data:
                service.description = update_data['description']
            if 'price' in update_data:
                service.price = update_data['price']
            if 'duration_minutes' in update_data:
                service.duration_minutes = update_data['duration_minutes']
            if 'department' in update_data:
                service.department = update_data['department']
            if 'image_url' in update_data:
                service.image_url = update_data.get('image_url', '')
            if 'category' in update_data:
                service.category_id = update_data['category']
            
            service.save()
            return service
            
        except Service.DoesNotExist:
            raise ValidationError("Servicio no encontrado")
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Error al actualizar el servicio: {str(e)}")
    
    @staticmethod
    def delete_service(service_id):
        """
        Elimina un servicio
        """
        try:
            service = Service.objects.get(id=service_id)
            service.delete()
            return True
        except Service.DoesNotExist:
            raise ValidationError("Servicio no encontrado")
    
    @staticmethod
    def search_services(search_term):
        """
        Busca servicios por nombre, descripción o departamento
        """
        return Service.objects.filter(
            Q(name__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(department__icontains=search_term)
        ).prefetch_related('categories')
    

    @staticmethod
    def get_services_by_duration(max_duration):
        """
        Obtiene servicios con duración menor o igual a la especificada
        """
        return Service.objects.filter(
            duration_minutes__lte=max_duration
        ).prefetch_related('categories').order_by('duration_minutes')
    
    @staticmethod
    def get_popular_services(limit=10):
        """
        Obtiene servicios populares (puedes personalizar la lógica de popularidad)
        """
        return Service.objects.all().prefetch_related('categories')[:limit]
    
    @staticmethod
    def get_services_with_category():
        """
        Obtiene todos los servicios que tienen categoría asignada
        """
        return Service.objects.filter(category__isnull=False).prefetch_related('categories')
    
    @staticmethod
    def get_services_without_category():
        """
        Obtiene todos los servicios sin categoría asignada
        """
        return Service.objects.filter(category__isnull=True)
    
    @staticmethod
    def get_services_by_ids(service_ids):
        """
        Obtiene servicios por una lista de IDs
        """
        return Service.objects.filter(id__in=service_ids).prefetch_related('categories')
    
    @staticmethod
    def get_service_count_by_department():
        """
        Obtiene el número de servicios por departamento
        """
        return Service.objects.values('department').annotate(count=models.Count('id'))
    
    @staticmethod
    def get_services_sorted_by_price(ascending=True):
        """
        Obtiene servicios ordenados por precio
        """
        order_by = 'price' if ascending else '-price'
        return Service.objects.all().prefetch_related('categories').order_by(order_by)
    
    @staticmethod
    def get_services_sorted_by_duration(ascending=True):
        """
        Obtiene servicios ordenados por duración
        """
        order_by = 'duration_minutes' if ascending else '-duration_minutes'
        return Service.objects.all().prefetch_related('categories').order_by(order_by)
