from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db.models import Q
import re
from django.contrib.auth import authenticate
from decimal import Decimal
from app.models import User
from app.models.user import RoleOptions
from app.repositories.user_repository import UserRepository

class UserService():
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, user_data):
        if self.user_repository.get_by_username(user_data["username"]) is not None:
          raise ValidationError("Username already in use")

        if self.user_repository.get_by_email(user_data["email"]) is not None:
          raise ValidationError("Email already in use")

        if user_data["password"] != user_data["confirm_password"]:
          raise ValidationError("Passwords do not match")


        data = user_data.copy()
        data.pop("confirm_password", None)

        return self.user_repository.create(**data)
