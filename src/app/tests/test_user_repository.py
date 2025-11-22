from app.models.user import User, RoleOptions
from app.repositories.user_repository import UserRepository
from django.test import TestCase

class TestUserRepository(TestCase):
    def setUp(self):
        self.repo = UserRepository()
        self.sample_data= {
                "username":"sofia",
                "last_name":"gomez",
                "address":"456 Elm St",
                "pay_method":"credit card",
                "role":RoleOptions.ADMIN
            }

    # def test_create_user(self):
    #     user = self.repo.create(**self.sample_data)

    #     test_user = User.objects.get(id = user.id)

    #     self.assertIsNotNone(test_user)
    #     self.assertIsNotNone(test_user.id)
    #     self.assertEqual(test_user.username, "sofia")

    def test_create_complete_user(self):
        user = self.repo.create(**self.sample_data)

        test_user = User.objects.get(id = user.id)

        self.assertIsNotNone(test_user.id)
        self.assertEqual(test_user.username, "sofia")
        self.assertEqual(test_user.last_name, "gomez")
        self.assertEqual(test_user.address, "456 Elm St")
        self.assertEqual(test_user.pay_method, "credit card")
        self.assertEqual(test_user.role, RoleOptions.ADMIN)
        
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
        user1 = User.objects.create(username="admin_user", role=RoleOptions.ADMIN)
        user2 = User.objects.create(username="normal_user", role=RoleOptions.USER)
        self.assertTrue(user1.is_admin())
        self.assertFalse(user2.is_admin())

    def test_get_by_email(self):
        user = User.objects.create(username="juan", email="juan@gmail.com")
        user_by_email = self.repo.get_by_email("juan@gmail.com")
        
        self.assertEqual(user, user_by_email)

    def test_get_by_username(self):
        test_username = "juan"

        user = User.objects.create(username=test_username)

        user_by_username = self.repo.get_by_username(test_username)

        self.assertEqual(user, user_by_username)



