from django.db import IntegrityError
from app.models.order import Order
from app.repositories.user_repository import UserRepository
from app.repositories.order_repository import OrderRepository
from django.test import TestCase

class TestOrderRepository(TestCase):
    def setUp(self):
        self.order_repo = OrderRepository()
        self.user_repo = UserRepository()
        self.user = self.user_repo.create(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

    def create_order(self, index=0):
        return self.order_repo.create(
            user_id=self.user.id,
            identifier=f"ORD1234{index}",
            address="123 Main St",
            payMethod="credit card"
        )

    def create_various_orders(self):
        orders = []
        for i in range(5):
            order = self.create_order(index=i)
            orders.append(order)
        return orders

    def test_create_order(self):
        order = self.create_order()
        self.assertIsNotNone(order.id)
        self.assertEqual(order.user_id, self.user.id)
        self.assertEqual(order.identifier, "ORD12340")
        self.assertEqual(order.status, Order.StatusOptions.PENDING)
        self.assertEqual(order.address, "123 Main St")
        self.assertEqual(order.payMethod, "credit card")

    def test_update_order(self):
        order = self.create_order()
        updated_order = self.order_repo.update(
            order.id,
            status=Order.StatusOptions.SHIPPED
        )
        self.assertEqual(updated_order.status, Order.StatusOptions.SHIPPED)

    def test_delete_order(self):
        order = self.create_order()
        deleted = self.order_repo.delete(order.id)
        self.assertTrue(deleted)
        self.assertEqual(Order.objects.count(), 0)

    def test_get_order_by_id(self):
        order = self.create_order()
        found_order = self.order_repo.get_order_by_id(order.id)
        self.assertEqual(found_order, order)

    def test_get_orders_by_user(self):
        user_id = self.user.id
        self.create_order()
        orders = self.order_repo.get_orders_by_user(user_id)
        self.assertIsNotNone(orders)

    def test_get_order_by_id(self):
        order = self.create_order()
        order = self.order_repo.get_order_by_id(order.id)
        self.assertIsNotNone(order)

    def test_get_orders_by_status(self):
        self.create_order()
        orders = self.order_repo.get_orders_by_status(Order.StatusOptions.PENDING)
        self.assertIsNotNone(orders)

    def test_get_orders_by_identifier(self):
        self.create_order()
        orders = self.order_repo.get_orders_by_identifier('ORD12345')
        self.assertIsNotNone(orders)

    def test_unique_identifier(self):
        order1 = self.create_order()
        with self.assertRaises(IntegrityError):
                order2 = self.create_order()
