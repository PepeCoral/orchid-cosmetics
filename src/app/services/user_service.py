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
        self.repository = UserRepository()
    
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Formato de email inválido")
        return True
    
    @staticmethod
    def validate_password(password, confirm_password):
        if len(password) < 6:
            raise ValidationError("La contraseña debe tener al menos 6 caracteres")
        if password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden")
        return True
    
    @staticmethod
    def create_user(user_data):
        try:
            # Validaciones básicas
            UserService.validate_email(user_data['email'])
            UserService.validate_password(user_data['password'], user_data['confirm_password'])
            
            # Verificar si el email ya existe
            if User.objects.filter(email=user_data['email']).exists():
                raise ValidationError("El email ya está registrado")
            print("creando usuario")
            # Crear usuario usando el método create_user de AbstractUser
            user = User.objects.create_user(
                username=user_data['username'],  
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data.get('last_name'),
                address=user_data.get('address', None),
                pay_method=user_data.get('pay_method', None),
                role=user_data.get('role', RoleOptions.USER)
            )
            
            return user
            
        except Exception as e:
            raise ValidationError(f"Error al crear usuario: {str(e)}")
    
    @staticmethod
    def authenticate_user(username, password):
        try:
            # Usar el sistema de autenticación de Django
            user = authenticate(username=username, password=password)
            print("autenticando usuario", user)
            if user is None:
                raise ValidationError("Credenciales inválidas")
            
            return user
        except Exception:
            raise ValidationError("Credenciales inválidas")
    
    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("Usuario no encontrado")
    
    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Usuario no encontrado")
        
    def get_user_by_username(username: str) -> User | None:
        try:
            return User.objects.get(username__exact=username)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def update_user(user_id, update_data):
        try:
            user = User.objects.get(id=user_id)
            
            # Validar email si se está actualizando
            if 'email' in update_data:
                UserService.validate_email(update_data['email'])
                if User.objects.filter(email=update_data['email']).exclude(id=user_id).exists():
                    raise ValidationError("El email ya está en uso")
                user.email = update_data['email']
                user.username = update_data['email']  # Actualizar username también
            
            # Actualizar campos según el modelo User
            if 'first_name' in update_data:
                user.first_name = update_data['first_name']
            if 'last_name' in update_data:
                user.last_name = update_data.get('last_name', '')
            if 'address' in update_data:
                user.address = update_data.get('address', '')
            if 'pay_method' in update_data:
                user.pay_method = update_data.get('pay_method', '')
            if 'role' in update_data:
                user.role = update_data.get('role', RoleOptions.USER)
            
            # Actualizar contraseña si se proporciona
            if 'password' in update_data:
                UserService.validate_password(update_data['password'], update_data['confirm_password'])
                user.set_password(update_data['password'])
            
            user.save()
            return user
            
        except User.DoesNotExist:
            raise ValidationError("Usuario no encontrado")
    
    @staticmethod
    def delete_user(user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            raise ValidationError("Usuario no encontrado")
    
    @staticmethod
    def get_all_users():
        return User.objects.all()
    
    @staticmethod
    def change_user_role(user_id, new_role):
        try:
            user = User.objects.get(id=user_id)
            
            # Validar que el rol sea uno de los permitidos
            valid_roles = [role.value for role in RoleOptions]
            if new_role not in valid_roles:
                raise ValidationError(f"Rol inválido. Roles permitidos: {', '.join(valid_roles)}")
            
            user.role = new_role
            user.save()
            return user
        except User.DoesNotExist:
            raise ValidationError("Usuario no encontrado")
    
    @staticmethod
    def search_users(search_term):
        """Busca usuarios por first_name, last_name o email"""
        return User.objects.filter(
            Q(first_name=search_term) |
            Q(last_name=search_term) |
            Q(email=search_term)
        )
    
    @staticmethod
    def get_admin_users():
        """Obtiene todos los usuarios administradores"""
        return User.objects.filter(role=RoleOptions.ADMIN)
    
    @staticmethod
    def get_regular_users():
        """Obtiene todos los usuarios regulares"""
        return User.objects.filter(role=RoleOptions.USER)
    
    @staticmethod
    def promote_to_admin(user_id):
        """Promueve un usuario a administrador"""
        return UserService.change_user_role(user_id, RoleOptions.ADMIN)
    
    @staticmethod
    def demote_to_user(user_id):
        """Degrada un administrador a usuario regular"""
        return UserService.change_user_role(user_id, RoleOptions.USER)