import pytest
from app.models.user import User, RoleOptions
from app.repositories.user_repository import UserRepository

@pytest.mark.django_db
class TestUserRepository:
    def setup_method(self):
        self.repo = UserRepository()

    def test_create_user(self):
        user = self.repo.create(first_name="juan")
        assert user.id is not None
        assert user.first_name == "juan"

    def test_create_complete_user(self):
        user = self.repo.create(
            first_name="sofia",
            last_name="gomez",
            address="456 Elm St",
            pay_method="credit card",
            role=RoleOptions.ADMIN
        )
        assert user.id is not None
        assert user.first_name == "sofia"
        assert user.last_name == "gomez"
        assert user.address == "456 Elm St"
        assert user.pay_method == "credit card"
        assert user.role == RoleOptions.ADMIN
        
    def test_get_all_users(self):
        User.objects.create(first_name="maria")
        User.objects.create(first_name="pedro")
        users = self.repo.get_all()
        assert users.count() == 2

    def test_get_address(self):
        User.objects.create(first_name="lucia", address="123 Main St")
        address = self.repo.get_address()
        assert address == "123 Main St"

    def test_get_by_id(self):
        user = User.objects.create(first_name="ana")
        found = self.repo.get_by_id(user.id)
        assert found == user

    def test_update_user(self):
        user = User.objects.create(first_name="luis")
        updated = self.repo.update(user.id, first_name="luis_updated")
        assert updated.first_name == "luis_updated"

    def test_delete_user(self):
        user = User.objects.create(first_name="carla")
        deleted = self.repo.delete(user.id)
        assert deleted is True
        assert User.objects.count() == 0


    def test_user_is_admin(self):
        user1 = User.objects.create(first_name="admin_user", role=RoleOptions.ADMIN)
        user2 = User.objects.create(first_name="normal_user", role=RoleOptions.USER)
        assert self.repo.is_admin(user1.role) is True
        assert self.repo.is_admin(user2.role) is False


