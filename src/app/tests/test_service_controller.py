import json
from decimal import Decimal
from django.test import RequestFactory, TestCase
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock
from app.models import Service, Category
from app.views import *
from app.services import user_service, service_service
from app.views.service_controller import create_service, delete_service, get_popular_services, get_service, get_services_by_category, get_services_by_department, get_services_by_duration, get_services_by_price_range, get_services_sorted_by_duration, get_services_sorted_by_price, list_services, search_services, service_categories_overview, update_service


class TestServiceController(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        
        # Crear categoría de prueba
        self.category = Category.objects.create(
            name="Hair Care"
        )
        
        # Datos de servicio válidos
        self.valid_service_data = {
            'name': 'Hair Cut',
            'description': 'Professional hair cutting service',
            'price': '25.00',
            'duration_minutes': 30,
            'department': 'Hair Salon',
            'image_url': 'https://example.com/haircut.jpg',
            'category': self.category.id
        }

    @patch('app.views.ServiceService.create_service')
    def test_create_service_success(self, mock_create_service):
        """Test de creación exitosa de servicio"""
        # Mock del servicio creado
        mock_service = MagicMock()
        mock_service.id = 1
        mock_service.name = 'Hair Cut'
        mock_service.description = 'Professional hair cutting service'
        mock_service.price = Decimal('25.00')
        mock_service.duration_minutes = 30
        mock_service.department = 'Hair Salon'
        mock_service.image_url = 'https://example.com/haircut.jpg'
        mock_service.category_id = self.category.id
        mock_service.category = self.category
        mock_create_service.return_value = mock_service
        
        request = self.factory.post(
            '/services/create/',
            data=json.dumps(self.valid_service_data),
            content_type='application/json'
        )
        
        response = create_service(request)
        
        assert response.status_code == 201
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['message'] == 'Servicio creado exitosamente'
        assert response_data['service']['name'] == 'Hair Cut'
        mock_create_service.assert_called_once_with(self.valid_service_data)

    @patch('app.views.ServiceService.create_service')
    def test_create_service_validation_error(self, mock_create_service):
        """Test de creación con error de validación"""
        mock_create_service.side_effect = ValidationError("Nombre inválido")
        
        request = self.factory.post(
            '/services/create/',
            data=json.dumps(self.valid_service_data),
            content_type='application/json'
        )
        
        response = create_service(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'error' in response_data

    @patch('app.views.ServiceService.create_service')
    def test_create_service_exception(self, mock_create_service):
        """Test de creación con excepción general"""
        mock_create_service.side_effect = Exception("Error de base de datos")
        
        request = self.factory.post(
            '/services/create/',
            data=json.dumps(self.valid_service_data),
            content_type='application/json'
        )
        
        response = create_service(request)
        
        assert response.status_code == 500
        response_data = json.loads(response.content)
        assert response_data['success'] == False

    @patch('app.views.ServiceService.get_service_by_id')
    def test_get_service_success(self, mock_get_service):
        """Test de obtención exitosa de servicio"""
        mock_service = MagicMock()
        mock_service.id = 1
        mock_service.name = 'Hair Cut'
        mock_service.description = 'Professional service'
        mock_service.price = Decimal('25.00')
        mock_service.duration_minutes = 30
        mock_service.department = 'Hair Salon'
        mock_service.image_url = 'https://example.com/image.jpg'
        mock_service.category_id = self.category.id
        mock_service.category = self.category
        mock_service.created_at = MagicMock(isoformat=lambda: '2023-01-01T00:00:00')
        mock_get_service.return_value = mock_service
        
        request = self.factory.get('/services/1/')
        response = get_service(request, 1)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['service']['name'] == 'Hair Cut'
        assert response_data['service']['category_name'] == 'Hair Care'

    @patch('app.views.ServiceService.get_service_by_id')
    def test_get_service_not_found(self, mock_get_service):
        """Test de obtención de servicio inexistente"""
        mock_get_service.side_effect = ValidationError("Servicio no encontrado")
        
        request = self.factory.get('/services/999/')
        response = get_service(request, 999)
        
        assert response.status_code == 404
        response_data = json.loads(response.content)
        assert response_data['success'] == False

    @patch('app.views.ServiceService.get_all_services')
    def test_list_services_success(self, mock_get_all_services):
        """Test de listado exitoso de servicios"""
        mock_services = [
            MagicMock(
                id=1,
                name='Service 1',
                description='Desc 1',
                price=Decimal('20.00'),
                duration_minutes=30,
                department='Dept 1',
                image_url='',
                category_id=self.category.id,
                category=self.category
            ),
            MagicMock(
                id=2,
                name='Service 2',
                description='Desc 2',
                price=Decimal('30.00'),
                duration_minutes=45,
                department='Dept 2',
                image_url='',
                category_id=None,
                category=None
            )
        ]
        mock_get_all_services.return_value = mock_services
        
        request = self.factory.get('/services/')
        response = list_services(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert len(response_data['services']) == 2
        assert response_data['count'] == 2

    @patch('app.views.ServiceService.get_services_by_category')
    def test_get_services_by_category_success(self, mock_get_by_category):
        """Test de obtención de servicios por categoría exitosa"""
        mock_services = [
            MagicMock(
                id=1,
                name='Service 1',
                description='Desc 1',
                price=Decimal('20.00'),
                duration_minutes=30,
                department='Dept 1',
                image_url='',
                category_id=self.category.id,
                category=self.category
            )
        ]
        mock_get_by_category.return_value = mock_services
        
        request = self.factory.get('/services/category/1/')
        response = get_services_by_category(request, 1)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['category_id'] == 1
        assert len(response_data['services']) == 1

    @patch('app.views.ServiceService.get_services_by_category')
    def test_get_services_by_category_not_found(self, mock_get_by_category):
        """Test de obtención de servicios por categoría inexistente"""
        mock_get_by_category.side_effect = ValidationError("Categoría no encontrada")
        
        request = self.factory.get('/services/category/999/')
        response = get_services_by_category(request, 999)
        
        assert response.status_code == 404
        response_data = json.loads(response.content)
        assert response_data['success'] == False

    @patch('app.views.ServiceService.get_services_by_department')
    def test_get_services_by_department_success(self, mock_get_by_department):
        """Test de obtención de servicios por departamento"""
        mock_services = [
            MagicMock(
                id=1,
                name='Hair Service',
                description='Hair desc',
                price=Decimal('25.00'),
                duration_minutes=30,
                department='Hair Salon',
                image_url='',
                category_id=self.category.id,
                category=self.category
            )
        ]
        mock_get_by_department.return_value = mock_services
        
        request = self.factory.get('/services/department/Hair%20Salon/')
        response = get_services_by_department(request, 'Hair Salon')
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['department'] == 'Hair Salon'
        assert len(response_data['services']) == 1

    @patch('app.views.ServiceService.update_service')
    def test_update_service_success(self, mock_update_service):
        """Test de actualización exitosa de servicio"""
        mock_updated_service = MagicMock()
        mock_updated_service.id = 1
        mock_updated_service.name = 'Updated Service'
        mock_updated_service.description = 'Updated description'
        mock_updated_service.price = Decimal('30.00')
        mock_updated_service.duration_minutes = 45
        mock_updated_service.department = 'Updated Dept'
        mock_updated_service.image_url = ''
        mock_updated_service.category_id = self.category.id
        mock_updated_service.category = self.category
        mock_update_service.return_value = mock_updated_service
        
        update_data = {
            'name': 'Updated Service',
            'price': '30.00',
            'duration_minutes': 45
        }
        
        request = self.factory.patch(
            '/services/1/update/',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        response = update_service(request, 1)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['message'] == 'Servicio actualizado exitosamente'
        assert response_data['service']['name'] == 'Updated Service'

    @patch('app.views.ServiceService.update_service')
    def test_update_service_validation_error(self, mock_update_service):
        """Test de actualización con error de validación"""
        mock_update_service.side_effect = ValidationError("Nombre duplicado")
        
        update_data = {'name': 'Duplicate Name'}
        
        request = self.factory.patch(
            '/services/1/update/',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        response = service_service.update_service(request, 1)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False

    @patch('app.views.ServiceService.delete_service')
    def test_delete_service_success(self, mock_delete_service):
        """Test de eliminación exitosa de servicio"""
        mock_delete_service.return_value = True
        
        request = self.factory.delete('/services/1/delete/')
        response = delete_service(request, 1)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['message'] == 'Servicio eliminado exitosamente'

    @patch('app.views.ServiceService.delete_service')
    def test_delete_service_not_found(self, mock_delete_service):
        """Test de eliminación de servicio inexistente"""
        mock_delete_service.side_effect = ValidationError("Servicio no encontrado")
        
        request = self.factory.delete('/services/999/delete/')
        response = delete_service(request, 999)
        
        assert response.status_code == 404
        response_data = json.loads(response.content)
        assert response_data['success'] == False

    @patch('app.views.ServiceService.search_services')
    def test_search_services_success(self, mock_search_services):
        """Test de búsqueda exitosa de servicios"""
        mock_services = [
            MagicMock(
                id=1,
                name='Hair Cut',
                description='Hair cutting service',
                price=Decimal('25.00'),
                duration_minutes=30,
                department='Hair Salon',
                image_url='',
                category_id=self.category.id,
                category=self.category
            )
        ]
        mock_search_services.return_value = mock_services
        
        request = self.factory.get('/services/search/?q=hair')
        response = search_services(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['search_term'] == 'hair'
        assert len(response_data['services']) == 1

    def test_search_services_missing_query(self):
        """Test de búsqueda sin parámetro de búsqueda"""
        request = self.factory.get('/services/search/')
        response = search_services(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'parámetro de búsqueda' in response_data['error']

    @patch('app.views.ServiceService.get_services_by_price_range')
    def test_get_services_by_price_range_success(self, mock_get_by_price):
        """Test de obtención por rango de precios exitosa"""
        mock_services = [
            MagicMock(
                id=1,
                name='Service 1',
                description='Desc 1',
                price=Decimal('25.00'),
                duration_minutes=30,
                department='Dept 1',
                image_url='',
                category_id=self.category.id,
                category=self.category
            )
        ]
        mock_get_by_price.return_value = mock_services
        
        request = self.factory.get('/services/price-range/?min_price=20&max_price=30')
        response = get_services_by_price_range(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['price_range']['min_price'] == '20'
        assert response_data['price_range']['max_price'] == '30'

    def test_get_services_by_price_range_missing_params(self):
        """Test de obtención por rango de precios sin parámetros"""
        request = self.factory.get('/services/price-range/')
        response = get_services_by_price_range(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'min_price y max_price son requeridos' in response_data['error']

    def test_get_services_by_price_range_invalid_prices(self):
        """Test de obtención por rango de precios con precios inválidos"""
        request = self.factory.get('/services/price-range/?min_price=invalid&max_price=30')
        response = get_services_by_price_range(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'precios deben ser números válidos' in response_data['error']

    @patch('app.views.ServiceService.get_services_by_price_range')
    def test_get_services_by_price_range_validation_error(self, mock_get_by_price):
        """Test de obtención por rango de precios con error de validación"""
        mock_get_by_price.side_effect = ValidationError("Precio mínimo mayor al máximo")
        
        request = self.factory.get('/services/price-range/?min_price=50&max_price=20')
        response = get_services_by_price_range(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False

    @patch('app.views.ServiceService.get_services_by_duration')
    def test_get_services_by_duration_success(self, mock_get_by_duration):
        """Test de obtención por duración exitosa"""
        mock_services = [
            MagicMock(
                id=1,
                name='Quick Service',
                description='Quick desc',
                price=Decimal('15.00'),
                duration_minutes=15,
                department='Dept 1',
                image_url='',
                category_id=self.category.id,
                category=self.category
            )
        ]
        mock_get_by_duration.return_value = mock_services
        
        request = self.factory.get('/services/duration/?max_duration=30')
        response = get_services_by_duration(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['max_duration'] == 30

    def test_get_services_by_duration_missing_param(self):
        """Test de obtención por duración sin parámetro"""
        request = self.factory.get('/services/duration/')
        response = get_services_by_duration(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'max_duration es requerido' in response_data['error']

    def test_get_services_by_duration_invalid_duration(self):
        """Test de obtención por duración con duración inválida"""
        request = self.factory.get('/services/duration/?max_duration=invalid')
        response = get_services_by_duration(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'duración debe ser un número entero válido' in response_data['error']

    @patch('app.views.ServiceService.get_popular_services')
    def test_get_popular_services_success(self, mock_get_popular):
        """Test de obtención de servicios populares"""
        mock_services = [
            MagicMock(
                id=1,
                name='Popular Service',
                description='Popular desc',
                price=Decimal('25.00'),
                duration_minutes=30,
                department='Dept 1',
                image_url='',
                category_id=self.category.id,
                category=self.category
            )
        ]
        mock_get_popular.return_value = mock_services
        
        request = self.factory.get('/services/popular/?limit=5')
        response = get_popular_services(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['limit'] == 5

    @patch('app.views.ServiceService.get_popular_services')
    def test_get_popular_services_default_limit(self, mock_get_popular):
        """Test de obtención de servicios populares con límite por defecto"""
        mock_services = []
        mock_get_popular.return_value = mock_services
        
        request = self.factory.get('/services/popular/')
        response = get_popular_services(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['limit'] == 10

    @patch('app.views.ServiceService.get_popular_services')
    def test_get_popular_services_invalid_limit(self, mock_get_popular):
        """Test de obtención de servicios populares con límite inválido"""
        mock_services = []
        mock_get_popular.return_value = mock_services
        
        request = self.factory.get('/services/popular/?limit=invalid')
        response = get_popular_services(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['limit'] == 10  # Debería usar el valor por defecto

    @patch('app.views.ServiceService.get_services_sorted_by_price')
    def test_get_services_sorted_by_price_ascending(self, mock_sorted_price):
        """Test de servicios ordenados por precio ascendente"""
        mock_services = [
            MagicMock(
                id=1,
                name='Cheap Service',
                description='Desc 1',
                price=Decimal('10.00'),
                duration_minutes=15,
                department='Dept 1',
                image_url='',
                category_id=self.category.id,
                category=self.category
            ),
            MagicMock(
                id=2,
                name='Expensive Service',
                description='Desc 2',
                price=Decimal('50.00'),
                duration_minutes=60,
                department='Dept 2',
                image_url='',
                category_id=self.category.id,
                category=self.category
            )
        ]
        mock_sorted_price.return_value = mock_services
        
        request = self.factory.get('/services/sorted/price/?order=asc')
        response = get_services_sorted_by_price(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['order'] == 'ascending'

    @patch('app.views.ServiceService.get_services_sorted_by_price')
    def test_get_services_sorted_by_price_descending(self, mock_sorted_price):
        """Test de servicios ordenados por precio descendente"""
        mock_services = []
        mock_sorted_price.return_value = mock_services
        
        request = self.factory.get('/services/sorted/price/?order=desc')
        response = get_services_sorted_by_price(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['order'] == 'descending'

    @patch('app.views.ServiceService.get_services_sorted_by_duration')
    def test_get_services_sorted_by_duration(self, mock_sorted_duration):
        """Test de servicios ordenados por duración"""
        mock_services = []
        mock_sorted_duration.return_value = mock_services
        
        request = self.factory.get('/services/sorted/duration/')
        response = get_services_sorted_by_duration(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True

    @patch('app.views.ServiceService.get_services_with_category')
    @patch('app.views.ServiceService.get_services_without_category')
    def test_service_categories_overview(self, mock_without_category, mock_with_category):
        """Test de resumen de servicios por categoría"""
        mock_with_category.return_value = [
            MagicMock(id=1, name='Service 1', category=self.category)
        ]
        mock_without_category.return_value = [
            MagicMock(id=2, name='Service 2')
        ]
        
        request = self.factory.get('/services/categories-overview/')
        response = service_categories_overview(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['with_category']['count'] == 1
        assert response_data['without_category']['count'] == 1
        assert response_data['total_services'] == 2

    # Tests para métodos HTTP no permitidos
    def test_create_service_wrong_method(self):
        """Test de creación con método HTTP incorrecto"""
        request = self.factory.get('/services/create/')
        response = create_service(request)
        assert response.status_code == 405  # Method Not Allowed

    def test_update_service_wrong_method(self):
        """Test de actualización con método HTTP incorrecto"""
        request = self.factory.get('/services/1/update/')
        response = update_service(request, 1)
        assert response.status_code == 405

    def test_delete_service_wrong_method(self):
        """Test de eliminación con método HTTP incorrecto"""
        request = self.factory.get('/services/1/delete/')
        response = delete_service(request, 1)
        assert response.status_code == 405