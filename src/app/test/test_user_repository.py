import pytest
from app.models.user import User
from app.repositories.user_repository import UserRepository

@pytest.mark.django_db
class TestUserRepository:
    def setup_method(self):
        self.repo = UserRepository()

    def test_create_user(self):
        user = self.repo.create(username="juan",)
        assert user.id is not None
        assert user.username == "juan"

    def test_create_complete_user(self):
        user = self.repo.create(
            username="sofia",
            last_name="gomez",
            address="456 Elm St",
            pay_method="credit card",
            role=User.RoleOptions.ADMIN
        )
        assert user.id is not None
        assert user.username == "sofia"
        assert user.last_name == "gomez"
        assert user.address == "456 Elm St"
        assert user.pay_method == "credit card"
        assert user.role == User.RoleOptions.ADMIN
        
    def test_get_all_users(self):
        User.objects.create(username="maria")
        User.objects.create(username="pedro")
        users = self.repo.get_all()
        assert users.count() == 2

    def test_get_address(self):
        User.objects.create(username="lucia", address="123 Main St")
        address = self.repo.get_address()
        assert address == "123 Main St"

    def test_get_by_id(self):
        user = User.objects.create(username="ana")
        found = self.repo.get_by_id(user.id)
        assert found == user

    def test_update_user(self):
        user = User.objects.create(username="luis")
        updated = self.repo.update(user.id, username="luis_updated")
        assert updated.username == "luis_updated"

    def test_delete_user(self):
        user = User.objects.create(username="carla")
        deleted = self.repo.delete(user.id)
        assert deleted is True
        assert User.objects.count() == 0


    def test_user_is_admin(self):
        user1 = User.objects.create(username="admin_user", role=User.RoleOptions.ADMIN)
        user2 = User.objects.create(username="normal_user", role=User.RoleOptions.USER)
        assert self.repo.is_admin(user1.role) is True
        assert self.repo.is_admin(user2.role) is False


