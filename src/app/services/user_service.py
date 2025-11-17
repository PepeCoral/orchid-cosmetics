from app.models.user import RoleOptions, User
from app.repositories.user_repository import UserRepository
from django.core.exceptions import ValidationError, PermissionDenied

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

    def update_user(self, user_id, user_data, request_user):
        user_to_update = self.user_repository.get_by_id(user_id)
        if not user_to_update:
            raise ValidationError("Usuario no encontrado.")

        if request_user.id != user_to_update.id:
            raise PermissionDenied("Solo puedes modificar tu propio perfil.")

        if 'username' in user_data:
            existing_user = self.user_repository.get_by_username(user_data["username"])
            if existing_user and existing_user.id != user_id:
                raise ValidationError("Username already in use")

        if 'email' in user_data:
            existing_user = self.user_repository.get_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValidationError("Email already in use")

        if 'password' in user_data and user_data['password']:
            user_to_update.set_password(user_data['password'])
            user_to_update.save()
            user_data.pop('password', None)

        return self.user_repository.update(user_id, **user_data)

    def delete_user(self, user_id, request_user):
        user_to_delete = self.user_repository.get_by_id(user_id)
        if not user_to_delete:
            raise ValidationError("Usuario no encontrado.")

        if request_user.id != user_to_delete.id:
            raise PermissionDenied("Solo puedes eliminar tu propio perfil.")

        return self.user_repository.delete(user_id)