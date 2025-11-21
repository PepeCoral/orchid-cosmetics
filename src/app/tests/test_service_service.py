from decimal import Decimal
from PIL import Image
from io import BytesIO
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.utils.datastructures import MultiValueDict
from django.test import TestCase, RequestFactory
from app.models import Service, Category
from app.services.service_service import ServiceService
from app.repositories.service_repository import ServiceRepository
class TestServiceService(TestCase):

    def setUp(self):
        """Configuración inicial para cada test"""
        self.category = Category.objects.create(name="Hair Care")
        self.service_service = ServiceService()
        self.service_repository = ServiceRepository()
        self.factory = RequestFactory()
        self.request = self.factory.post(
            path="tests-service-service",
            FILES={}
        )
        self.categories = Category.objects.all()
        
        self.valid_service_data = {
            'name': 'Hair Cut',
            'description': 'Professional hair cutting service',
            'price': 25.00,
            'duration_minutes': 30,
            'department': 'Hair Salon',
            'image_url': '',
            'categories': self.categories
        }
        self.updated_service_data = {
            'name': 'Hair Cut Updated',
            'description': 'Professional hair cutting service Updated',
            'price': 35.00,
            'duration_minutes': 40,
            'department': 'Hair Salon Updated'
        }

    def generar_imagen(self):
        imagen = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        imagen.save(buffer, format="JPEG")
        buffer.seek(0)

        return InMemoryUploadedFile(
            file=buffer,
            field_name="imagen",
            name="test.jpg",
            content_type="image/jpeg",
            size=buffer.getbuffer().nbytes,
            charset=None
        )

    def test_create_service_success(self):

        service = self.service_service.create_service(self.request,self.valid_service_data)
    
        assert service.name == self.valid_service_data['name']
        assert service.description == self.valid_service_data['description']
        assert service.price == self.valid_service_data['price']
        assert service.duration_minutes == self.valid_service_data['duration_minutes']
        assert service.department == self.valid_service_data['department']
        #assert service.image_url == fake_file
        assert set(service.categories.all()) == set(self.categories)

    def test_create_service_wrong_data(self):

        wrong_data = self.valid_service_data.copy()
        wrong_data['price'] = -5.0
        
        with self.assertRaises(ValidationError, msg="Price cannot be negative"):
            self.service_service.create_service(self.request,wrong_data)

        wrong_data['price'] = 10.0
        wrong_data['duration_minutes'] = -5

        with self.assertRaises(ValidationError, msg="Duration cannot be negative"):
            self.service_service.create_service(self.request,wrong_data)


    def test_get_service_by_id_success(self):
        created = self.service_service.create_service(self.request,self.valid_service_data)
        found = self.service_service.get_service_by_id(created.id)
        
        self.assertEqual(found,created)

    def test_get_service_by_id_not_found(self):
        with self.assertRaises(ValidationError, msg="Servicio no encontrado"):
            self.service_service.get_service_by_id(999)

    def test_get_all_services(self):
        
        service_data1 = self.valid_service_data.copy()
        service_data2 = self.valid_service_data.copy()

        self.service_service.create_service(self.request,service_data1)
        self.service_service.create_service(self.request,service_data2)

        all_services = self.service_service.get_all_services()
        self.assertEqual(all_services.count(),2)

    def test_update_service_success(self):
        
        service_data = self.valid_service_data.copy()
        updated_data = self.updated_service_data.copy()

        service = self.service_service.create_service(self.request, service_data)

        updated = self.service_service.update_service(service.id, updated_data, self.request)
        
        self.assertEqual(updated.name,'Hair Cut Updated')
        self.assertEqual(updated.description,'Professional hair cutting service Updated')
        self.assertEqual(updated.price,35.00)
        self.assertEqual(updated.duration_minutes,40)
        self.assertEqual(updated.department,'Hair Salon Updated')

    def test_update_service_wrong_data(self):
        

        wrong_data = self.valid_service_data.copy()

        service = self.service_service.create_service(self.request, wrong_data)

        wrong_data['price'] = -5.0
        
        with self.assertRaises(ValidationError, msg="El precio no puede ser negativo"):
            self.service_service.update_service(service.id,wrong_data, self.request)

        wrong_data['price'] = 10.0
        wrong_data['duration_minutes'] = -5

        with self.assertRaises(ValidationError, msg="La duración no puede ser negativa"):
            self.service_service.update_service(service.id,wrong_data, self.request)

    def test_update_service_not_found(self):
        
        with self.assertRaises(ValidationError, msg="Servicio no encontrado"):
            self.service_service.update_service(999, {'name': 'Updated'}, self.request)

    def test_delete_service_success(self):
        service = self.service_service.create_service(self.request,self.valid_service_data)
        
        result = self.service_service.delete_service(service.id)
        assert result is True

    def test_delete_service_not_found(self):
        with self.assertRaises(ValidationError, msg="Servicio no encontrado."):
            self.service_service.delete_service(999)

    def test_search_services_by_name(self):
        data_list = [
            {'name': 'Hair Cut', 'description': 'Cutting hair', 'price': 25.00, 'duration_minutes': 30, 'department': 'Hair', 'categories':self.categories},
            {'name': 'Hair Color', 'description': 'Coloring hair', 'price': 50.00, 'duration_minutes': 60, 'department': 'Hair','categories':self.categories},
            {'name': 'Facial', 'description': 'Face treatment', 'price': 40.00, 'duration_minutes': 45, 'department': 'Spa','categories':self.categories}
        ]
        
        for d in data_list:
            self.service_service.create_service(self.request,d)
        
        filters = {'name':'Hair'}

        assert self.service_service.search_services(filters).count() == 2

    def test_search_services_by_department(self):
        data_list = [
            {'name': 'Service 1', 'description': 'Desc 1', 'price': 25.00, 'duration_minutes': 30, 'department': 'Hair Salon','categories':self.categories},
            {'name': 'Service 2', 'description': 'Desc 2', 'price': 40.00, 'duration_minutes': 45, 'department': 'Spa','categories':self.categories},
            {'name': 'Service 3', 'description': 'Desc 3', 'price': 30.00, 'duration_minutes': 40, 'department': 'Hair Salon','categories':self.categories}
        ]
        
        for d in data_list:
            self.service_service.create_service(self.request,d)
        
        filters = {'department':'Salon'}

        assert self.service_service.search_services(filters).count() == 2

    def test_get_promoted_services(self):
        service_data1 = self.valid_service_data.copy()
        service_data2 = self.valid_service_data.copy()

        service_data2['isPromoted'] = True

        self.service_service.create_service(self.request,service_data1)
        self.service_service.create_service(self.request,service_data2)

        promoted_services = self.service_service.get_promoted_services()

        self.assertEqual(promoted_services.count(),1)

    def test_promote_service(self):
        service_data = self.valid_service_data.copy()

        service = self.service_service.create_service(self.request,service_data)

        self.service_service.promote_service(service.id)

        promoted = self.service_service.get_service_by_id(service.id)

        self.assertEqual(promoted.isPromoted, True)

    def test_demote_service(self):
        service_data = self.valid_service_data.copy()

        service_data['isPromoted']=True
        service = self.service_service.create_service(self.request,service_data)

        self.service_service.demote_service(service.id)

        promoted = self.service_service.get_service_by_id(service.id)

        self.assertEqual(promoted.isPromoted, False)

    def test_promote_an_invalid_service(self):
        with self.assertRaises(ValidationError,msg="Servicio no encontrado."):
            self.service_service.promote_service(999)
    
    def test_demote_an_invalid_service(self):
        with self.assertRaises(ValidationError,msg="Servicio no encontrado."):
            self.service_service.demote_service(999)

