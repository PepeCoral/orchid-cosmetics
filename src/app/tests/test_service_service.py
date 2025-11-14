from decimal import Decimal
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock

from django.test import TestCase
from app.models import Service, Category
from app.services.service_service import ServiceService

class TestServiceService(TestCase):

    def setUp(self):
        """Configuración inicial para cada test"""
        self.category = Category.objects.create(name="Hair Care")
        
        self.valid_service_data = {
            'name': 'Hair Cut',
            'description': 'Professional hair cutting service',
            'price': 25.00,
            'duration_minutes': 30,
            'department': 'Hair Salon',
            'image_url': 'https://example.com/haircut.jpg',
            'category': self.category.id
        }

    def test_validate_service_data_success(self):
        ServiceService.validate_service_data(self.valid_service_data)

    def test_validate_service_data_missing_name(self):
        data = self.valid_service_data.copy()
        data['name'] = ''
        
        with self.assertRaises(ValidationError, msg="Nombre faltante"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_name_too_long(self):
        data = self.valid_service_data.copy()
        data['name'] = 'A' * 101
        
        with self.assertRaises(ValidationError, msg="Nombre demasiado largo"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_missing_description(self):
        data = self.valid_service_data.copy()
        data['description'] = ''
        
        with self.assertRaises(ValidationError, msg="Descripción faltante"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_invalid_price(self):
        data = self.valid_service_data.copy()
        data['price'] = Decimal('-10.00')
        
        with self.assertRaises(ValidationError, msg="Precio negativo no permitido"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_price_zero(self):
        data = self.valid_service_data.copy()
        data['price'] = Decimal('0.00')
        
        with self.assertRaises(ValidationError, msg="Precio cero inválido"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_price_string(self):
        data = self.valid_service_data.copy()
        data['price'] = 'invalid'
        
        with self.assertRaises(ValidationError, msg="Precio debe ser numérico"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_missing_duration(self):
        data = self.valid_service_data.copy()
        data['duration_minutes'] = None
        
        with self.assertRaises(ValidationError, msg="Duración faltante"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_duration_negative(self):
        data = self.valid_service_data.copy()
        data['duration_minutes'] = -10
        
        with self.assertRaises(ValidationError, msg="Duración negativa inválida"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_duration_string(self):
        data = self.valid_service_data.copy()
        data['duration_minutes'] = 'invalid'
        
        with self.assertRaises(ValidationError, msg="Duración debe ser numérica"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_missing_department(self):
        data = self.valid_service_data.copy()
        data['department'] = ''
        
        with self.assertRaises(ValidationError, msg="Departamento faltante"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_department_too_long(self):
        data = self.valid_service_data.copy()
        data['department'] = 'A' * 101
        
        with self.assertRaises(ValidationError, msg="Departamento demasiado largo"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_invalid_category(self):
        data = self.valid_service_data.copy()
        data['category'] = 999
        
        with self.assertRaises(ValidationError, msg="Categoría inexistente"):
            ServiceService.validate_service_data(data)

    def test_validate_service_data_image_url_too_long(self):
        data = self.valid_service_data.copy()
        data['image_url'] = 'https://example.com/' + 'a' * 200
        
        with self.assertRaises(ValidationError, msg="URL demasiado larga"):
            ServiceService.validate_service_data(data)

    def test_create_service_success(self):
        service = ServiceService.create_service(self.valid_service_data)
        
        assert service.name == self.valid_service_data['name']
        assert service.description == self.valid_service_data['description']
        assert service.price == self.valid_service_data['price']
        assert service.duration_minutes == self.valid_service_data['duration_minutes']
        assert service.department == self.valid_service_data['department']
        assert service.image_url == self.valid_service_data['image_url']
        assert service.category.id == self.valid_service_data['category']

    def test_create_service_duplicate_name(self):
        ServiceService.create_service(self.valid_service_data)
        
        with self.assertRaises(ValidationError, msg="Nombre duplicado"):
            ServiceService.create_service(self.valid_service_data)

    def test_create_service_without_category(self):
        data = self.valid_service_data.copy()
        data.pop('category')
        
        service = ServiceService.create_service(data)
        
        assert service.name == data['name']
        assert service.category is None

    def test_create_service_without_image_url(self):
        data = self.valid_service_data.copy()
        data.pop('image_url')
        
        service = ServiceService.create_service(data)
        
        assert service.name == data['name']
        assert service.image_url == ''

    def test_get_service_by_id_success(self):
        created = ServiceService.create_service(self.valid_service_data)
        found = ServiceService.get_service_by_id(created.id)
        
        assert found == created

    def test_get_service_by_id_not_found(self):
        with self.assertRaises(ValidationError, msg="Servicio no encontrado"):
            ServiceService.get_service_by_id(999)

    def test_get_all_services(self):
        services_data = [
            {
                'name': f'Service {i}',
                'description': f'Description {i}',
                'price': (i+1)*10.00,
                'duration_minutes': (i+1) * 15,
                'department': f'Department {i % 2}',
                'category': self.category.id
            }
            for i in range(3)
        ]
        
        created = [ServiceService.create_service(d) for d in services_data]
        
        all_services = ServiceService.get_all_services()
        assert all_services.count() == 3

    def test_get_services_by_category_success(self):
        for i in range(2):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            ServiceService.create_service(data)
        
        services = ServiceService.get_services_by_category(self.category.id)
        assert services.count() == 2

    def test_get_services_by_category_not_found(self):
        with self.assertRaises(ValidationError, msg="Categoría no encontrada"):
            ServiceService.get_services_by_category(999)

    def test_get_services_by_department(self):
        departments = ['Hair Salon', 'Spa', 'Hair Salon']
        for i, d in enumerate(departments):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['department'] = d
            ServiceService.create_service(data)
        
        assert ServiceService.get_services_by_department('Hair Salon').count() == 2
        assert ServiceService.get_services_by_department('Spa').count() == 1

    def test_get_services_by_department_case_insensitive(self):
        data = self.valid_service_data.copy()
        data['department'] = 'HAIR SALON'
        ServiceService.create_service(data)
        
        assert ServiceService.get_services_by_department('hair salon').count() == 1

    def test_update_service_success(self):
        service = ServiceService.create_service(self.valid_service_data)
        
        update_data = {
            'name': 'Updated Hair Cut',
            'description': 'Updated description',
            'price': 30.00,
            'duration_minutes': 45,
            'department': 'Updated Department'
        }
        
        updated = ServiceService.update_service(service.id, update_data)
        
        assert updated.name == 'Updated Hair Cut'

    def test_update_service_duplicate_name(self):
        s1 = ServiceService.create_service(self.valid_service_data)
        
        data2 = self.valid_service_data.copy()
        data2['name'] = 'Other Service'
        s2 = ServiceService.create_service(data2)
        
        with self.assertRaises(ValidationError, msg="Nombre duplicado en actualización"):
            ServiceService.update_service(s2.id, {'name': 'Hair Cut'})

    def test_update_service_not_found(self):
        with self.assertRaises(ValidationError, msg="Servicio no encontrado"):
            ServiceService.update_service(999, {'name': 'Updated'})

    def test_delete_service_success(self):
        service = ServiceService.create_service(self.valid_service_data)
        
        result = ServiceService.delete_service(service.id)
        assert result is True
        
        with self.assertRaises(ValidationError):
            ServiceService.get_service_by_id(service.id)

    def test_delete_service_not_found(self):
        with self.assertRaises(ValidationError, msg="Servicio no encontrado"):
            ServiceService.delete_service(999)

    def test_search_services_by_name(self):
        data_list = [
            {'name': 'Hair Cut', 'description': 'Cutting hair', 'price': 25.00, 'duration_minutes': 30, 'department': 'Hair'},
            {'name': 'Hair Color', 'description': 'Coloring hair', 'price': 50.00, 'duration_minutes': 60, 'department': 'Hair'},
            {'name': 'Facial', 'description': 'Face treatment', 'price': 40.00, 'duration_minutes': 45, 'department': 'Spa'}
        ]
        
        for d in data_list:
            ServiceService.create_service(d)
        
        assert ServiceService.search_services('Hair').count() == 2

    def test_search_services_by_description(self):
        data_list = [
            {'name': 'Service 1', 'description': 'Hair cutting service', 'price': 25.00, 'duration_minutes': 30, 'department': 'Hair'},
            {'name': 'Service 2', 'description': 'Face treatment service', 'price': 40.00, 'duration_minutes': 45, 'department': 'Spa'}
        ]
        
        for d in data_list:
            ServiceService.create_service(d)
        
        results = ServiceService.search_services('treatment')
        assert results.count() == 1

    def test_search_services_by_department(self):
        data_list = [
            {'name': 'Service 1', 'description': 'Desc 1', 'price': 25.00, 'duration_minutes': 30, 'department': 'Hair Salon'},
            {'name': 'Service 2', 'description': 'Desc 2', 'price': 40.00, 'duration_minutes': 45, 'department': 'Spa'},
            {'name': 'Service 3', 'description': 'Desc 3', 'price': 30.00, 'duration_minutes': 40, 'department': 'Hair Salon'}
        ]
        
        for d in data_list:
            ServiceService.create_service(d)
        
        assert ServiceService.search_services('Salon').count() == 2

    def test_get_services_by_price_range_success(self):
        prices = [20.00, 30.00, 40.00, 50.00]
        for i, p in enumerate(prices):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['price'] = p
            ServiceService.create_service(data)
        
        results = ServiceService.get_services_by_price_range(Decimal('25.00'), Decimal('45.00'))
        assert results.count() == 2

    def test_get_services_by_price_range_invalid(self):
        with self.assertRaises(ValidationError, msg="Rango de precios inválido"):
            ServiceService.get_services_by_price_range(Decimal('50.00'), Decimal('25.00'))

    def test_get_services_by_duration(self):
        durations = [15, 30, 45, 60]
        for i, d in enumerate(durations):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['duration_minutes'] = d
            ServiceService.create_service(data)
        
        results = ServiceService.get_services_by_duration(30)
        assert results.count() == 2

    def test_get_popular_services(self):
        for i in range(15):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            ServiceService.create_service(data)
        
        assert ServiceService.get_popular_services(limit=10).count() == 10

    def test_get_services_with_category(self):
        ServiceService.create_service(self.valid_service_data)
        
        no_cat = self.valid_service_data.copy()
        no_cat['name'] = 'No Category Service'
        no_cat.pop('category')
        ServiceService.create_service(no_cat)
        
        results = ServiceService.get_services_with_category()
        assert results.count() == 1

    def test_get_services_without_category(self):
        ServiceService.create_service(self.valid_service_data)
        
        no_cat = self.valid_service_data.copy()
        no_cat['name'] = 'No Category Service'
        no_cat.pop('category')
        ServiceService.create_service(no_cat)
        
        results = ServiceService.get_services_without_category()
        assert results.count() == 1

    def test_get_services_by_ids(self):
        services = []
        for i in range(3):
            d = self.valid_service_data.copy()
            d['name'] = f'Service {i}'
            services.append(ServiceService.create_service(d))
        
        ids = [services[0].id, services[2].id]
        results = ServiceService.get_services_by_ids(ids)
        
        assert results.count() == 2

    def test_get_services_sorted_by_price_ascending(self):
        prices = [50.00, 20.00, 35.00]
        for i, p in enumerate(prices):
            d = self.valid_service_data.copy()
            d['name'] = f'Service {i}'
            d['price'] = p
            ServiceService.create_service(d)
        
        results = ServiceService.get_services_sorted_by_price(True)
        assert results.first().price == 20.00

    def test_get_services_sorted_by_price_descending(self):
        prices = [20.00, 50.00, 35.00]
        for i, p in enumerate(prices):
            d = self.valid_service_data.copy()
            d['name'] = f'Service {i}'
            d['price'] = p
            ServiceService.create_service(d)
        
        results = ServiceService.get_services_sorted_by_price(False)
        assert results.first().price == 50.00

    def test_get_services_sorted_by_duration_ascending(self):
        durations = [60, 15, 45]
        for i, d in enumerate(durations):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['duration_minutes'] = d
            ServiceService.create_service(data)
        
        results = ServiceService.get_services_sorted_by_duration(True)
        assert results.first().duration_minutes == 15

    def test_get_services_sorted_by_duration_descending(self):
        durations = [15, 60, 45]
        for i, d in enumerate(durations):
            data = self.valid_service_data.copy()
            data['name'] = f'Service {i}'
            data['duration_minutes'] = d
            ServiceService.create_service(data)
        
        results = ServiceService.get_services_sorted_by_duration(False)
        assert results.first().duration_minutes == 60
