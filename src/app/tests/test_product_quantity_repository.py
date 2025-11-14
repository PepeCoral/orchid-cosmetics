from app.models.product import ProductQuantity
from app.repositories.product_quantity_repository import ProductQuantityRepository
from app.repositories.user_repository import UserRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from django.test import TestCase

class TestProductQuantityRepository(TestCase):
    def setUp(self):
        self.quantity_repo = ProductQuantityRepository()
        self.product_repo = ProductRepository()
        self.order_repo = OrderRepository()
        self.user_repo = UserRepository()
        self.category_repo = CategoryRepository()
        self.category = self.category_repo.create(name="Test Category")
        self.user = self.user_repo.create(
            username="testuser", email="testuser@example.com", password="password")
        self.product = self.product_repo.create(
            name="Test Product",
            description="Product Description", stock=100, category_id=1,
            price=10.0, fabricator="Test Fabricator",
            image_url="http://example.com/image.jpg")
        self.order = self.order_repo.create(
            user_id=self.user.id, address="123 Test St", status="pending",
            payMethod="credit card", identifier="ORD12345", delivery_method="standard")

    def test_create_product_quantity(self):
        pq = self.quantity_repo.create(
            product_id=self.product.id,
            order_id=self.order.id,
            quantity=5
        )
        self.assertIsNotNone(pq.id)
        self.assertEqual(pq.product_id, self.product.id)
        self.assertEqual(pq.order_id, self.order.id)
        self.assertEqual(pq.quantity, 5)

    def create_product_quantity(self, quantity=2):
        return self.quantity_repo.create(
            product_id=self.product.id,
            order_id=self.order.id,
            quantity=quantity
        )

    def test_get_by_id(self):
        pq = self.create_product_quantity(quantity=4)
        found = self.quantity_repo.get_by_id(pq.id)
        self.assertEqual(found, pq)

    def test_get_all_product_quantities(self):
        self.create_product_quantity(quantity=5)
        self.create_product_quantity(quantity=10)
        quantities = self.quantity_repo.get_all()
        self.assertEqual(quantities.count(), 2)

    def test_update_product_quantity(self):
        pq = self.create_product_quantity(quantity=3)
        updated = self.quantity_repo.update(pq.id, quantity=8)
        self.assertEqual(updated.quantity, 8)

    def test_delete_product_quantity(self):
        pq = self.create_product_quantity(quantity=6)
        deleted = self.quantity_repo.delete(pq.id)
        self.assertTrue(deleted)
        self.assertEqual(ProductQuantity.objects.count(), 0)
    
    def test_get_total_quantity_of_a_product(self):
        self.create_product_quantity(quantity=3)
        total_quantity = self.quantity_repo.get_total_quantity_of_a_product(product_id=self.product.id, order_id=self.order.id)
        self.assertIsNotNone(total_quantity)
