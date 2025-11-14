from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Q
from app import models
from app.models import Service, Category


class ServiceService():
    
    @staticmethod
    def validate_service_data(service_data):
        errors = {}
        
        if not service_data.get('name') or len(service_data['name'].strip()) == 0:
            errors['name'] = "El nombre es obligatorio"
        elif len(service_data['name']) > 100:
            errors['name'] = "El nombre no puede tener más de 100 caracteres"

        if not service_data.get('description') or len(service_data['description'].strip()) == 0:
            errors['description'] = "La descripción es obligatoria"
        
        # Validar precio
        price = service_data.get('price')
        if price is None:
            errors['price'] = "El precio es obligatorio"
        elif not isinstance(price,float):
            errors['price'] = "Precio debe ser numérico"
        else:
            try:
                price_decimal = Decimal(str(price))
                if price_decimal <= 0:
                    errors['price'] = "El precio debe ser mayor a 0"
                if price_decimal.as_tuple().exponent < -2:
                    errors['price'] = "El precio no puede tener más de 2 decimales"
            except (ValueError, TypeError):
                errors['price'] = "El precio debe ser un número válido"
        
        # Validar duración
        duration = service_data.get('duration_minutes')
        if duration is None:
            errors['duration_minutes'] = "La duración es obligatoria"
        else:
            try:
                duration_int = int(duration)
                if duration_int <= 0:
                    errors['duration_minutes'] = "La duración debe ser mayor a 0 minutos"
            except (ValueError, TypeError):
                errors['duration_minutes'] = "La duración debe ser un número entero válido"
        
        # Validar departamento
        if not service_data.get('department') or len(service_data['department'].strip()) == 0:
            errors['department'] = "El departamento es obligatorio"
        elif len(service_data['department']) > 100:
            errors['department'] = "El departamento no puede tener más de 100 caracteres"

        # Validar categoría
        category_id = service_data.get('category')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                errors['category'] = "La categoría especificada no existe"
        
        # Validar image_url
        image_url = service_data.get('image_url', '')
        if image_url and len(image_url) > 200:
            errors['image_url'] = "La URL de la imagen no puede tener más de 200 caracteres"
        
        if errors:
            raise ValidationError(errors)
        
    @staticmethod
    def create_service(service_data):
        """
        Crea un nuevo servicio
        """
        try:
            ServiceService.validate_service_data(service_data)

            # Verificar si ya existe un servicio con el mismo nombre
            if Service.objects.filter(name=service_data['name']).exists():
                raise ValidationError("Ya existe un servicio con este nombre")

            service = Service(
                name=service_data['name'],
                description=service_data['description'],
                price=service_data['price'],
                duration_minutes=service_data['duration_minutes'],
                department=service_data['department'],
                image_url=service_data.get('image_url', ''),
                category_id=service_data.get('category')
            )
            
            service.save()
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
        return Service.objects.all().select_related('category')
    
    @staticmethod
    def get_services_by_category(category_id):
        """
        Obtiene servicios por categoría
        """
        try:
            category = Category.objects.get(id=category_id)
            return Service.objects.filter(category=category).select_related('category')
        except Category.DoesNotExist:
            raise ValidationError("Categoría no encontrada")
    
    @staticmethod
    def get_services_by_department(department):
        """
        Obtiene servicios por departamento (case-insensitive)
        """
        return Service.objects.filter(department__iexact=department).select_related('category')
    
    @staticmethod
    def update_service(service_id, update_data):
        """
        Actualiza un servicio existente
        """
        try:
            service = Service.objects.get(id=service_id)
            
            # Preparar datos para validación
            data_to_validate = {
                'name': update_data.get('name', service.name),
                'description': update_data.get('description', service.description),
                'price': update_data.get('price', service.price),
                'duration_minutes': update_data.get('duration_minutes', service.duration_minutes),
                'department': update_data.get('department', service.department),
                'category': update_data.get('category', service.category_id),
                'image_url': update_data.get('image_url', service.image_url)
            }
            
            ServiceService.validate_service_data(data_to_validate)
            
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
        ).select_related('category')
    
    @staticmethod
    def get_services_by_price_range(min_price, max_price):
        """
        Obtiene servicios dentro de un rango de precios
        """
        if min_price > max_price:
            raise ValidationError("El precio mínimo no puede ser mayor al precio máximo")
        
        return Service.objects.filter(
            price__gte=min_price,
            price__lte=max_price
        ).select_related('category').order_by('price')
    
    @staticmethod
    def get_services_by_duration(max_duration):
        """
        Obtiene servicios con duración menor o igual a la especificada
        """
        return Service.objects.filter(
            duration_minutes__lte=max_duration
        ).select_related('category').order_by('duration_minutes')
    
    @staticmethod
    def get_popular_services(limit=10):
        """
        Obtiene servicios populares (puedes personalizar la lógica de popularidad)
        """
        return Service.objects.all().select_related('category')[:limit]
    
    @staticmethod
    def get_services_with_category():
        """
        Obtiene todos los servicios que tienen categoría asignada
        """
        return Service.objects.filter(category__isnull=False).select_related('category')
    
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
        return Service.objects.filter(id__in=service_ids).select_related('category')
    
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
        return Service.objects.all().select_related('category').order_by(order_by)
    
    @staticmethod
    def get_services_sorted_by_duration(ascending=True):
        """
        Obtiene servicios ordenados por duración
        """
        order_by = 'duration_minutes' if ascending else '-duration_minutes'
        return Service.objects.all().select_related('category').order_by(order_by)