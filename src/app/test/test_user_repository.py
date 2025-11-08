from app.models.user import User
from app.repositories.user_repository import UserRepository
from django.test import TestCase

class TestUserRepository(TestCase):
    def setUp(self):
        self.repo = UserRepository()

    def test_create_user(self):
        user = self.repo.create(username="juan",)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "juan")

    def test_create_complete_user(self):
        user = self.repo.create(
            username="sofia",
            last_name="gomez",
            address="456 Elm St",
            pay_method="credit card",
            role=User.RoleOptions.ADMIN
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "sofia")
        self.assertEqual(user.last_name, "gomez")
        self.assertEqual(user.address, "456 Elm St")
        self.assertEqual(user.pay_method, "credit card")
        self.assertEqual(user.role, User.RoleOptions.ADMIN)
        
    def test_get_all_users(self):
        User.objects.create(username="maria")
        User.objects.create(username="pedro")
        users = self.repo.get_all()
        self.assertEqual(users.count(), 2)

    def test_get_by_id(self):
        user = User.objects.create(username="ana")
        found = self.repo.get_by_id(user.id)
        self.assertEqual(found, user)

    def test_update_user(self):
        user = User.objects.create(username="luis")
        updated = self.repo.update(user.id, username="luis_updated")
        self.assertEqual(updated.username, "luis_updated")

    def test_delete_user(self):
        user = User.objects.create(username="carla")
        deleted = self.repo.delete(user.id)
        self.assertTrue(deleted)
        self.assertEqual(User.objects.count(), 0)


    def test_user_is_admin(self):
        user1 = User.objects.create(username="admin_user", role=User.RoleOptions.ADMIN)
        user2 = User.objects.create(username="normal_user", role=User.RoleOptions.USER)
        self.assertTrue(user1.is_admin())
        self.assertFalse(user2.is_admin())


