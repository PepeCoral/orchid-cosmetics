import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock
from app.models import Service, Category
from app.services.service_service import ServiceService

@pytest.mark.django_db
class TestServiceService:

    def setup_method(self):
        """Configuración inicial para cada test"""
        # Crear categoría de prueba
        self.category = Category.objects.create(
            name="Hair Care",
            description="Hair services"
        )
        
        # Datos de servicio válidos
        self.valid_service_data = {
            'name': 'Hair Cut',
            'description': 'Professional hair cutting service',
            'price': Decimal('25.00'),
            'duration_minutes': 30,
            'department': 'Hair Salon',
            'image_url': 'https://example.com/haircut.jpg',
            'category': self.category.id
        }

    def test_validate_service_data_success(self):
        """Test de validación exitosa de datos de servicio"""
        ServiceService.validate_service_data(self.valid_service_data)
        # Si no hay excepción, la validación pasó

    def test_validate_service_data_missing_name(self):
        """Test de validación con nombre faltante"""
        data = self.valid_service_data.copy()
        data['name'] = ''
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'name' in str(exc_info.value)

    def test_validate_service_data_name_too_long(self):
        """Test de validación con nombre muy largo"""
        data = self.valid_service_data.copy()
        data['name'] = 'A' * 101
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'nombre no puede tener más de 100 caracteres' in str(exc_info.value)

    def test_validate_service_data_missing_description(self):
        """Test de validación con descripción faltante"""
        data = self.valid_service_data.copy()
        data['description'] = ''
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'descripción' in str(exc_info.value)

    def test_validate_service_data_invalid_price(self):
        """Test de validación con precio inválido"""
        # Precio negativo
        data = self.valid_service_data.copy()
        data['price'] = Decimal('-10.00')
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'precio debe ser mayor a 0' in str(exc_info.value)

    def test_validate_service_data_price_zero(self):
        """Test de validación con precio cero"""
        data = self.valid_service_data.copy()
        data['price'] = Decimal('0.00')
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'precio debe ser mayor a 0' in str(exc_info.value)

    def test_validate_service_data_price_string(self):
        """Test de validación con precio como string"""
        data = self.valid_service_data.copy()
        data['price'] = 'invalid'
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'precio debe ser un número válido' in str(exc_info.value)

    def test_validate_service_data_missing_duration(self):
        """Test de validación con duración faltante"""
        data = self.valid_service_data.copy()
        data['duration_minutes'] = None
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'duración' in str(exc_info.value)

    def test_validate_service_data_duration_negative(self):
        """Test de validación con duración negativa"""
        data = self.valid_service_data.copy()
        data['duration_minutes'] = -10
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'duración debe ser mayor a 0 minutos' in str(exc_info.value)

    def test_validate_service_data_duration_string(self):
        """Test de validación con duración como string inválido"""
        data = self.valid_service_data.copy()
        data['duration_minutes'] = 'invalid'
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'duración debe ser un número entero válido' in str(exc_info.value)

    def test_validate_service_data_missing_department(self):
        """Test de validación con departamento faltante"""
        data = self.valid_service_data.copy()
        data['department'] = ''
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'departamento' in str(exc_info.value)

    def test_validate_service_data_department_too_long(self):
        """Test de validación con departamento muy largo"""
        data = self.valid_service_data.copy()
        data['department'] = 'A' * 101
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'departamento no puede tener más de 100 caracteres' in str(exc_info.value)

    def test_validate_service_data_invalid_category(self):
        """Test de validación con categoría inválida"""
        data = self.valid_service_data.copy()
        data['category'] = 999  # ID que no existe
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'categoría especificada no existe' in str(exc_info.value)

    def test_validate_service_data_image_url_too_long(self):
        """Test de validación con URL de imagen muy larga"""
        data = self.valid_service_data.copy()
        data['image_url'] = 'https://example.com/' + 'a' * 200
        
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.validate_service_data(data)
        
        assert 'URL de la imagen no puede tener más de 200 caracteres' in str(exc_info.value)

    def test_create_service_success(self):
        """Test de creación exitosa de servicio"""
        service = ServiceService.create_service(self.valid_service_data)
        
        assert service.name == self.valid_service_data['name']
        assert service.description == self.valid_service_data['description']
        assert service.price == self.valid_service_data['price']
        assert service.duration_minutes == self.valid_service_data['duration_minutes']
        assert service.department == self.valid_service_data['department']
        assert service.image_url == self.valid_service_data['image_url']
        assert service.category.id == self.valid_service_data['category']

    def test_create_service_duplicate_name(self):
        """Test que evita crear servicios con nombre duplicado"""
        # Crear primer servicio
        ServiceService.create_service(self.valid_service_data)
        
        # Intentar crear segundo servicio con mismo nombre
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.create_service(self.valid_service_data)
        
        assert 'Ya existe un servicio con este nombre' in str(exc_info.value)

    def test_create_service_without_category(self):
        """Test de creación de servicio sin categoría"""
        data = self.valid_service_data.copy()
        data.pop('category')  # Remover categoría
        
        service = ServiceService.create_service(data)
        
        assert service.name == data['name']
        assert service.category is None

    def test_create_service_without_image_url(self):
        """Test de creación de servicio sin URL de imagen"""
        data = self.valid_service_data.copy()
        data.pop('image_url')  # Remover image_url
        
        service = ServiceService.create_service(data)
        
        assert service.name == data['name']
        assert service.image_url == ''

    def test_get_service_by_id_success(self):
        """Test de obtención de servicio por ID"""
        created_service = ServiceService.create_service(self.valid_service_data)
        found_service = ServiceService.get_service_by_id(created_service.id)
        
        assert found_service == created_service

    def test_get_service_by_id_not_found(self):
        """Test de obtención de servicio por ID inexistente"""
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.get_service_by_id(999)
        
        assert 'Servicio no encontrado' in str(exc_info.value)

    def test_get_all_services(self):
        """Test de obtención de todos los servicios"""
        # Crear varios servicios
        services_data = [
            {
                'name': f'Service {i}',
                'description': f'Description {i}',
                'price': Decimal(f'{i * 10}.00'),
                'duration_minutes': i * 15,
                'department': f'Department {i % 2}',
                'category': self.category.id
            }
            for i in range(3)
        ]
        
        created_services = []
        for data in services_data:
            created_services.append(ServiceService.create_service(data))
        
        all_services = ServiceService.get_all_services()
        
        assert all_services.count() == 3
        for service in created_services:
            assert service in all_services

    def test_get_services_by_category_success(self):
        """Test de obtención de servicios por categoría"""
        # Crear servicios en la misma categoría
        for i in range(2):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            ServiceService.create_service(data)
        
        services = ServiceService.get_services_by_category(self.category.id)
        
        assert services.count() == 2
        for service in services:
            assert service.category == self.category

    def test_get_services_by_category_not_found(self):
        """Test de obtención de servicios por categoría inexistente"""
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.get_services_by_category(999)
        
        assert 'Categoría no encontrada' in str(exc_info.value)

    def test_get_services_by_department(self):
        """Test de obtención de servicios por departamento"""
        # Crear servicios en diferentes departamentos
        departments = ['Hair Salon', 'Spa', 'Hair Salon']
        for i, dept in enumerate(departments):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['department'] = dept
            ServiceService.create_service(data)
        
        hair_services = ServiceService.get_services_by_department('Hair Salon')
        assert hair_services.count() == 2
        
        spa_services = ServiceService.get_services_by_department('Spa')
        assert spa_services.count() == 1

    def test_get_services_by_department_case_insensitive(self):
        """Test de obtención de servicios por departamento (case insensitive)"""
        data = self.valid_service_data.copy()
        data['department'] = 'HAIR SALON'
        ServiceService.create_service(data)
        
        services = ServiceService.get_services_by_department('hair salon')
        assert services.count() == 1

    def test_update_service_success(self):
        """Test de actualización exitosa de servicio"""
        service = ServiceService.create_service(self.valid_service_data)
        
        update_data = {
            'name': 'Updated Hair Cut',
            'description': 'Updated description',
            'price': Decimal('30.00'),
            'duration_minutes': 45,
            'department': 'Updated Department'
        }
        
        updated_service = ServiceService.update_service(service.id, update_data)
        
        assert updated_service.name == 'Updated Hair Cut'
        assert updated_service.description == 'Updated description'
        assert updated_service.price == Decimal('30.00')
        assert updated_service.duration_minutes == 45
        assert updated_service.department == 'Updated Department'

    def test_update_service_duplicate_name(self):
        """Test que evita actualizar a un nombre duplicado"""
        # Crear primer servicio
        service1 = ServiceService.create_service(self.valid_service_data)
        
        # Crear segundo servicio
        data2 = self.valid_service_data.copy()
        data2['name'] = 'Other Service'
        service2 = ServiceService.create_service(data2)
        
        # Intentar cambiar nombre del segundo servicio al del primero
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.update_service(service2.id, {'name': 'Hair Cut'})
        
        assert 'Ya existe un servicio con este nombre' in str(exc_info.value)

    def test_update_service_not_found(self):
        """Test de actualización de servicio inexistente"""
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.update_service(999, {'name': 'Updated'})
        
        assert 'Servicio no encontrado' in str(exc_info.value)

    def test_delete_service_success(self):
        """Test de eliminación exitosa de servicio"""
        service = ServiceService.create_service(self.valid_service_data)
        
        result = ServiceService.delete_service(service.id)
        
        assert result == True
        # Verificar que el servicio ya no existe
        with pytest.raises(ValidationError):
            ServiceService.get_service_by_id(service.id)

    def test_delete_service_not_found(self):
        """Test de eliminación de servicio inexistente"""
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.delete_service(999)
        
        assert 'Servicio no encontrado' in str(exc_info.value)

    def test_search_services_by_name(self):
        """Test de búsqueda de servicios por nombre"""
        services_data = [
            {'name': 'Hair Cut', 'description': 'Cutting hair', 'price': Decimal('25.00'), 'duration_minutes': 30, 'department': 'Hair'},
            {'name': 'Hair Color', 'description': 'Coloring hair', 'price': Decimal('50.00'), 'duration_minutes': 60, 'department': 'Hair'},
            {'name': 'Facial', 'description': 'Face treatment', 'price': Decimal('40.00'), 'duration_minutes': 45, 'department': 'Spa'}
        ]
        
        for data in services_data:
            ServiceService.create_service(data)
        
        results = ServiceService.search_services('Hair')
        assert results.count() == 2

    def test_search_services_by_description(self):
        """Test de búsqueda de servicios por descripción"""
        services_data = [
            {'name': 'Service 1', 'description': 'Hair cutting service', 'price': Decimal('25.00'), 'duration_minutes': 30, 'department': 'Hair'},
            {'name': 'Service 2', 'description': 'Face treatment service', 'price': Decimal('40.00'), 'duration_minutes': 45, 'department': 'Spa'}
        ]
        
        for data in services_data:
            ServiceService.create_service(data)
        
        results = ServiceService.search_services('treatment')
        assert results.count() == 1
        assert results.first().name == 'Service 2'

    def test_search_services_by_department(self):
        """Test de búsqueda de servicios por departamento"""
        services_data = [
            {'name': 'Service 1', 'description': 'Desc 1', 'price': Decimal('25.00'), 'duration_minutes': 30, 'department': 'Hair Salon'},
            {'name': 'Service 2', 'description': 'Desc 2', 'price': Decimal('40.00'), 'duration_minutes': 45, 'department': 'Spa'},
            {'name': 'Service 3', 'description': 'Desc 3', 'price': Decimal('35.00'), 'duration_minutes': 40, 'department': 'Hair Salon'}
        ]
        
        for data in services_data:
            ServiceService.create_service(data)
        
        results = ServiceService.search_services('Salon')
        assert results.count() == 2

    def test_get_services_by_price_range_success(self):
        """Test de obtención de servicios por rango de precios"""
        prices = [Decimal('20.00'), Decimal('30.00'), Decimal('40.00'), Decimal('50.00')]
        for i, price in enumerate(prices):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['price'] = price
            ServiceService.create_service(data)
        
        results = ServiceService.get_services_by_price_range(Decimal('25.00'), Decimal('45.00'))
        assert results.count() == 2  # 30 y 40

    def test_get_services_by_price_range_invalid(self):
        """Test de obtención de servicios con rango de precios inválido"""
        with pytest.raises(ValidationError) as exc_info:
            ServiceService.get_services_by_price_range(Decimal('50.00'), Decimal('25.00'))
        
        assert 'precio mínimo no puede ser mayor al precio máximo' in str(exc_info.value)

    def test_get_services_by_duration(self):
        """Test de obtención de servicios por duración máxima"""
        durations = [15, 30, 45, 60]
        for i, duration in enumerate(durations):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['duration_minutes'] = duration
            ServiceService.create_service(data)
        
        results = ServiceService.get_services_by_duration(30)
        assert results.count() == 2  # 15 y 30

    def test_get_popular_services(self):
        """Test de obtención de servicios populares"""
        # Crear más de 10 servicios
        for i in range(15):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            ServiceService.create_service(data)
        
        popular_services = ServiceService.get_popular_services(limit=10)
        assert popular_services.count() == 10

    def test_get_services_with_category(self):
        """Test de obtención de servicios con categoría"""
        # Crear servicio con categoría
        ServiceService.create_service(self.valid_service_data)
        
        # Crear servicio sin categoría
        data_no_category = self.valid_service_data.copy()
        data_no_category['name'] = 'No Category Service'
        data_no_category.pop('category')
        ServiceService.create_service(data_no_category)
        
        services_with_category = ServiceService.get_services_with_category()
        assert services_with_category.count() == 1
        assert services_with_category.first().name == 'Hair Cut'

    def test_get_services_without_category(self):
        """Test de obtención de servicios sin categoría"""
        # Crear servicio con categoría
        ServiceService.create_service(self.valid_service_data)
        
        # Crear servicio sin categoría
        data_no_category = self.valid_service_data.copy()
        data_no_category['name'] = 'No Category Service'
        data_no_category.pop('category')
        ServiceService.create_service(data_no_category)
        
        services_without_category = ServiceService.get_services_without_category()
        assert services_without_category.count() == 1
        assert services_without_category.first().name == 'No Category Service'

    def test_get_services_by_ids(self):
        """Test de obtención de servicios por lista de IDs"""
        services = []
        for i in range(3):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            services.append(ServiceService.create_service(data))
        
        service_ids = [services[0].id, services[2].id]
        results = ServiceService.get_services_by_ids(service_ids)
        
        assert results.count() == 2
        assert results.filter(id=services[0].id).exists()
        assert results.filter(id=services[2].id).exists()

    def test_get_services_sorted_by_price_ascending(self):
        """Test de obtención de servicios ordenados por precio ascendente"""
        prices = [Decimal('50.00'), Decimal('20.00'), Decimal('35.00')]
        for i, price in enumerate(prices):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['price'] = price
            ServiceService.create_service(data)
        
        results = ServiceService.get_services_sorted_by_price(ascending=True)
        assert results.first().price == Decimal('20.00')
        assert results.last().price == Decimal('50.00')

    def test_get_services_sorted_by_price_descending(self):
        """Test de obtención de servicios ordenados por precio descendente"""
        prices = [Decimal('20.00'), Decimal('50.00'), Decimal('35.00')]
        for i, price in enumerate(prices):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['price'] = price
            ServiceService.create_service(data)
        
        results = ServiceService.get_services_sorted_by_price(ascending=False)
        assert results.first().price == Decimal('50.00')
        assert results.last().price == Decimal('20.00')

    def test_get_services_sorted_by_duration_ascending(self):
        """Test de obtención de servicios ordenados por duración ascendente"""
        durations = [60, 15, 45]
        for i, duration in enumerate(durations):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['duration_minutes'] = duration
            ServiceService.create_service(data)
        
        results = ServiceService.get_services_sorted_by_duration(ascending=True)
        assert results.first().duration_minutes == 15
        assert results.last().duration_minutes == 60

    def test_get_services_sorted_by_duration_descending(self):
        """Test de obtención de servicios ordenados por duración descendente"""
        durations = [15, 60, 45]
        for i, duration in enumerate(durations):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['duration_minutes'] = duration
            ServiceService.create_service(data)
        
        results = ServiceService.get_services_sorted_by_duration(ascending=False)
        assert results.first().duration_minutes == 60
        assert results.last().duration_minutes == 15