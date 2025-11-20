from typing import Optional
from app.repositories.base_repository import BaseRepository
from app.models.user import User
from django.contrib.auth import authenticate

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email) -> Optional[User]:
        return self.model.objects.filter(email=email).first()

    def get_by_username(self,username) -> Optional[User]:
        return self.model.objects.filter(username=username).first()

    def create(self, **kwargs) -> User:
        return self.model.objects.create_user(**kwargs)

    def authenticate_user(self, email, password):
        user = User.objects.get(email=email)

        user_log = authenticate(username=user.username,password=password)

        return user_log