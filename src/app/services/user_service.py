from app.models.user import User
from app.repositories.user_repository import UserRepository
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth import login, authenticate


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

        is_super_user = False
        if len(self.user_repository.get_all()) == 0:
            is_super_user = True

        data = user_data.copy()
        data.pop("confirm_password", None)

        superuser=False
        if len(self.user_repository.get_all()) == 0:
            superuser=True

        user =  self.user_repository.create(**data)
        user.is_superuser = superuser
        user.save()
        return user

    def get_user_by_id(self, user_id):
      user = self.user_repository.get_by_id(user_id)
      if not user:
          raise ValidationError("Usuario no encontrado.")
      return user

    def authenticate_user(self, auth_data):
        email = auth_data['email']
        password = auth_data['password']

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValidationError("No hay ningun usuario con ese email")
        
        try:
            
            user_log = authenticate(username=user.username,password=password)
            return user_log
        
        except Exception as a:
            raise ValidationError("Ha habido un error en la autenticacion ", a)
        
    def update_user(self, user_id, user_data, request_user):
        user_to_update = self.user_repository.get_by_id(user_id)
        if not user_to_update:
            raise ValidationError("Usuario no encontrado.")
    
        if user_id != request_user.id:
            if not request_user.is_superuser:
                raise PermissionDenied("Solo puedes modificar tu propio perfil.")
            if user_to_update.is_superuser:
                raise PermissionDenied("No se puede modificar a otro admin.")
            
        # Hacer copia para no modificar el original
        update_data = user_data.copy()

        if 'username' in update_data:
            existing_user = self.user_repository.get_by_username(update_data["username"])
            if existing_user and existing_user.id != user_id:
                raise ValidationError("Username already in use")

        if 'email' in update_data:
            existing_user = self.user_repository.get_by_email(update_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValidationError("Email already in use")

        if 'password' in update_data and update_data['password']:
            # Verificar que no sea string vacío o solo espacios
            if update_data['password'].strip():
                user_to_update.set_password(update_data['password'])
                user_to_update.save()

        update_data.pop('password', None)

        # Actualizar otros campos
        updated_user = self.user_repository.update(user_id, **update_data)

        return updated_user

    def delete_user(self, user_id, request_user):
        user_to_delete = self.user_repository.get_by_id(user_id)
        if not user_to_delete:
            raise ValidationError("Usuario no encontrado.")

        if request_user.id != user_to_delete.id:
            if not request_user.is_superuser:
                raise PermissionDenied("Solo puedes eliminar tu propio perfil.")
            elif user_to_delete.is_superuser:
                raise PermissionDenied("No se puede eliminar a otro admin.")

        return self.user_repository.delete(user_id)
    
    def get_all_users(self):
        return self.user_repository.get_all()
