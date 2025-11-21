from app.models import Service, Category
from app.repositories.service_repository import ServiceRepository
from app.repositories.category_repository import CategoryRepository
from django.test import TestCase

class TestServiceRepository(TestCase):
    def setUp(self):
        super().setUp()
        self.service_repo = ServiceRepository()
        self.category_repo = CategoryRepository()
        self.service_data = {
            'name':'Massage',
            'description':"Relaxing full body massage",
            'price':75.00,
            'department':"Wellness",
            'duration_minutes':60,
            'image_url':"http://example.com/massage.jpg"
        }

    def create_service(self, service_data):

        service = self.service_repo.create(**service_data)
        
        categories = Category.objects.all()

        service.set_categories(categories)
        return service

    def test_create_service(self):
        service = self.create_service(self.service_data.copy())
        categories = Category.objects.all()

        self.assertIsNotNone(service.id)
        self.assertEqual(service.name, "Massage")
        self.assertEqual(service.description, "Relaxing full body massage")
        self.assertEqual(service.price, 75.00)
        self.assertEqual(set(categories),set(service.categories.all()))
        self.assertEqual(service.department, "Wellness")
        self.assertEqual(service.duration_minutes, 60)
        self.assertEqual(service.image_url, "http://example.com/massage.jpg")
        self.assertEqual(service.isPromoted,False)

    def test_get_service_by_id(self):
        service = self.create_service(self.service_data.copy())

        found = self.service_repo.get_by_id(service.id)
        self.assertEqual(found, service)

    def test_get_services_by_category(self):
        service_data1 = self.service_data.copy()
        service_data2 = self.service_data.copy()
        
        service_data2['name']='Otro servicio'

        self.create_service(service_data1)

        Category.objects.create(name="Especifico")
        
        categories1 = Category.objects.all()
        categories2 = Category.objects.filter(id=2)
        
        service2 = self.create_service(service_data2)
        
        service2.set_categories(categories2)

        services1 = self.service_repo.get_services_by_category_id(categories2.first().id)
        services2 = self.service_repo.get_services_by_category_id(categories2.first().id)
        
        self.assertEqual(services1.count(), 1)
        self.assertEqual(services2.count(), 1)

    def test_search_name(self):
        service_data1= self.service_data.copy()
        service_data2= self.service_data.copy()

        service_data2['name']='Massage 2'

        service1 = self.create_service(service_data1)
        service2 = self.create_service(service_data2)

        services1 = Service.objects.all()
        services2 = services1.exclude(id=service1.id)

        name_filters1 = {'name':'Massage'}
        name_filters2 = {'name':'Massage 2'}
        
        search1 = self.service_repo.search(name_filters1)
        search2 = self.service_repo.search(name_filters2)

        self.assertEqual(search1.count(),2)
        self.assertEqual(set(search1),set(services1))
        self.assertEqual(search2.count(),1)
        self.assertEqual(set(search2),set(services2))

    def test_search_min_max_price(self):
        service_data1= self.service_data.copy()
        service_data2= self.service_data.copy()
        service_data3= self.service_data.copy()

        service_data2['name']='Service 2'
        service_data2['price']=10.00
        service_data3['name']='Service 3'
        service_data3['price']=100.00

        service1 = self.create_service(service_data1)
        min_service = self.create_service(service_data2)
        max_service = self.create_service(service_data3)

        services = Service.objects.all()
        min_services = services.exclude(id=min_service.id)
        max_services = services.exclude(id=max_service.id)

        min_filters = {'min_price':35.00}
        max_filters = {'max_price':80.00}
        min_max_filters = {'min_price':45.00,'max_price':80.00}
        
        min_search = self.service_repo.search(min_filters)
        max_search = self.service_repo.search(max_filters)
        min_max_search = self.service_repo.search(min_max_filters)

        self.assertEqual(min_search.count(),2)
        self.assertEqual(set(min_search),set(min_services))
        self.assertEqual(max_search.count(),2)
        self.assertEqual(set(max_search),set(max_services))
        self.assertEqual(min_max_search.count(),1)
        self.assertEqual(min_max_search.first(),service1)

    def test_search_department(self):
        service_data1= self.service_data.copy()
        service_data2= self.service_data.copy()

        service_data2['department']='Wellness 2'

        service1 = self.create_service(service_data1)
        service2 = self.create_service(service_data2)

        services1 = Service.objects.all()
        services2 = services1.exclude(id=service1.id)

        department_filters1 = {'department':'Wellness'}
        department_filters2 = {'department':'Wellness 2'}
        
        search1 = self.service_repo.search(department_filters1)
        search2 = self.service_repo.search(department_filters2)

        self.assertEqual(search1.count(),2)
        self.assertEqual(set(search1),set(services1))
        self.assertEqual(search2.count(),1)
        self.assertEqual(set(search2),set(services2))

    def test_get_all_promoted_services(self):
        service_data1 = self.service_data.copy()
        service_data2 = self.service_data.copy()

        service_data2['isPromoted'] = True

        self.create_service(service_data1)
        self.create_service(service_data2)

        services = self.service_repo.get_all_promoted_services()

        self.assertEqual(services.count(),1)
    # def test_get_all_services(self):
    #     service_data = self.service_data.copy()
    #     self.create_service(service_data)
    #     service_data['name']='otro servicio'
    #     self.create_service(service_data)
    #     services = self.service_repo.get_all()
    #     self.assertEqual(services.count(), 2)
    #
    # def test_update_service(self):
    #     service = self.create_service(category=self.category1.id)
    #     updated = self.service_repo.update(
    #         service.id,
    #         name="Deep Tissue Massage",
    #         price=90.00
    #     )
    #     self.assertEqual(updated.name, "Deep Tissue Massage")
    #     self.assertEqual(updated.price, 90.00)
    #
    # def test_delete_service(self):
    #     service = self.create_service(category=self.category1.id)
    #     deleted = self.service_repo.delete(service.id)
    #     self.assertTrue(deleted)
    #     self.assertEqual(Service.objects.count(), 0)

    