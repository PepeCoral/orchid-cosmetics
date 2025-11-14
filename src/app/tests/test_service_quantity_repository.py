from app.models.service import ServiceQuantity
from app.repositories.service_quantity_repository import ServiceQuantityRepository
from app.repositories.user_repository import UserRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.service_repository import ServiceRepository
from app.repositories.category_repository import CategoryRepository
from django.test import TestCase

class TestServiceQuantityRepository(TestCase):
    def setUp(self):
        self.quantity_repo = ServiceQuantityRepository()
        self.service_repo = ServiceRepository()
        self.order_repo = OrderRepository()
        self.user_repo = UserRepository()
        self.category_repo = CategoryRepository()
        self.category = self.category_repo.create(name="Test Category")
        self.user = self.user_repo.create(
            username="testuser", email="testuser@example.com", password="password")
        self.service = self.service_repo.create(
            name="Test Service", description="Service Description", price=20.0,
            duration_minutes=60, department="Test Department",
            category_id=1, image_url="http://example.com/service.jpg")
        self.order = self.order_repo.create(
            user_id=self.user.id, address="123 Test St", status="pending",
            payMethod="credit card", identifier="ORD12345", delivery_method="standard")

    def test_create_service_quantity(self):
        sq = self.quantity_repo.create(
            service_id=self.service.id,
            order_id=self.order.id,
            quantity=5
        )
        self.assertIsNotNone(sq.id)
        self.assertEqual(sq.service_id, self.service.id)
        self.assertEqual(sq.order_id, self.order.id)
        self.assertEqual(sq.quantity, 5)
    
    def create_service_quantity(self, quantity=3):
        return self.quantity_repo.create(
            service_id=self.service.id,
            order_id=self.order.id,
            quantity=quantity
        )

    def test_get_by_id(self):
        sq = self.create_service_quantity(quantity=4)
        found = self.quantity_repo.get_by_id(sq.id)
        self.assertEqual(found, sq)

    def test_get_all_service_quantities(self):
        self.create_service_quantity(quantity=5)
        self.create_service_quantity(quantity=10)
        quantities = self.quantity_repo.get_all()
        self.assertEqual(quantities.count(), 2)

    def test_update_service_quantity(self):
        sq = self.create_service_quantity(quantity=3)
        updated = self.quantity_repo.update(sq.id, quantity=8)
        self.assertEqual(updated.quantity, 8)

    def test_delete_service_quantity(self):
        sq = self.create_service_quantity(quantity=6)
        deleted = self.quantity_repo.delete(sq.id)
        self.assertTrue(deleted)
        self.assertEqual(ServiceQuantity.objects.count(), 0)

    def test_get_total_quantity_of_a_service(self):
        self.create_service_quantity(quantity=2)
        total_quantity = self.quantity_repo.get_total_quantity_of_a_service(service_id=self.service.id, order_id=self.order.id)
        self.assertIsNotNone(total_quantity)