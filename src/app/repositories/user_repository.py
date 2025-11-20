from typing import Optional
from app.repositories.base_repository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
        self.user=User

    def get_by_email(self, email) -> User:
        return self.user.objects.filter(email=email).first()

    def get_by_username(self,username) -> User:
        return self.user.objects.filter(username=username).first()

    def create(self, **kwargs) -> User:
        return self.user.objects.create_user(**kwargs)
