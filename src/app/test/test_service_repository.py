from app.models import Service, Category
from app.repositories.service_repository import ServiceRepository
from app.repositories.category_repository import CategoryRepository
from django.test import TestCase

class TestServiceRepository(TestCase):
    def setUp(self):
        super().setUp()
        self.service_repo = ServiceRepository()
        self.category_repo = CategoryRepository()
        self.category1 = self.category_repo.create(name="Health")
        self.category2 = self.category_repo.create(name="Beauty")

    def create_category(self, name="Health"):
        return self.category_repo.create(name=name)

    def create_service(self, name="Massage", category = None):
        
        return self.service_repo.create(
            name=name,
            description="Relaxing full body massage",
            price=75.00,
            category_id=category,
            department="Wellness",
            duration_minutes=60,
            image_url="http://example.com/massage.jpg"
        )
    
    def test_create_service(self):
        service = self.create_service(category=self.category1.id)
        self.assertIsNotNone(service.id)
        self.assertEqual(service.name, "Massage")
        self.assertEqual(service.description, "Relaxing full body massage")
        self.assertEqual(service.price, 75.00)
        self.assertEqual(service.category.name, "Health")
        self.assertEqual(service.department, "Wellness")
        self.assertEqual(service.duration_minutes, 60)
        self.assertEqual(service.image_url, "http://example.com/massage.jpg")

    def test_get_service_by_id(self):
        service = self.create_service(category=self.category1.id)
        found = self.service_repo.get_by_id(service.id)
        self.assertEqual(found, service)

    def test_get_all_services(self):
        self.create_service(name="Facial", category=self.category2.id)
        self.create_service(name="Manicure", category=self.category2.id)
        services = self.service_repo.get_all()
        self.assertEqual(services.count(), 2)

    def test_update_service(self):
        service = self.create_service(category=self.category1.id)
        updated = self.service_repo.update(
            service.id,
            name="Deep Tissue Massage",
            price=90.00
        )
        self.assertEqual(updated.name, "Deep Tissue Massage")
        self.assertEqual(updated.price, 90.00)

    def test_delete_service(self):
        service = self.create_service(category=self.category1.id)
        deleted = self.service_repo.delete(service.id)
        self.assertTrue(deleted)
        self.assertEqual(Service.objects.count(), 0)

    def test_get_services_by_category(self):
        self.create_service(name="Yoga Class", category=self.category1.id)
        self.create_service(name="Pilates Class", category=self.category1.id)
        self.create_service(name="Haircut", category=self.category2.id)
        services = self.service_repo.get_services_by_category(self.category1.id)
        print("AAAAAAAAAAAAAAAAAAAAAAAAA")
        print(services)
        self.assertEqual(services.count(), 2)