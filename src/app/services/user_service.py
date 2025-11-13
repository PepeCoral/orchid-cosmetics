from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db.models import Q 
from .models import User
import re
from .models import Service, Category
from decimal import Decimal


class UserService:
    
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Formato de email inválido")
        return True
    
    @staticmethod
    def validate_password(password):
        if len(password) < 6:
            raise ValidationError("La contraseña debe tener al menos 6 caracteres")
        return True
    
    @staticmethod
    def create_user(user_data):
        try:
            # Validaciones básicas
            UserService.validate_email(user_data['email'])
            UserService.validate_password(user_data['password'])
            
            # Verificar si el email ya existe
            if User.objects.filter(email=user_data['email']).exists():
                raise ValidationError("El email ya está registrado")
            
            # Hashear contraseña
            hashed_password = make_password(user_data['password'])
            
            # Crear usuario con el modelo existente
            user = User(
                name=user_data['name'],
                surname=user_data.get('surname', ''),
                email=user_data['email'],
                password=hashed_password,
                address=user_data.get('address', ''),
                payMethod=user_data.get('payMethod', ''),
                role=user_data.get('role', '')  # Rol vacío por defecto como en el modelo
            )
            
            user.save()
            return user
            
        except Exception as e:
            raise ValidationError(f"Error al crear usuario: {str(e)}")
    
    @staticmethod
    def authenticate_user(email, password):
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return user
            else:
                raise ValidationError("Credenciales inválidas")
        except User.DoesNotExist:
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
            
            # Actualizar otros campos según el modelo existente
            if 'name' in update_data:
                user.name = update_data['name']
            if 'surname' in update_data:
                user.surname = update_data.get('surname', '')
            if 'address' in update_data:
                user.address = update_data.get('address', '')
            if 'payMethod' in update_data:
                user.payMethod = update_data.get('payMethod', '')
            if 'role' in update_data:
                user.role = update_data.get('role', '')
            
            # Hashear nueva contraseña si se proporciona
            if 'password' in update_data:
                UserService.validate_password(update_data['password'])
                user.password = make_password(update_data['password'])
            
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
            user.role = new_role
            user.save()
            return user
        except User.DoesNotExist:
            raise ValidationError("Usuario no encontrado")
    
    @staticmethod
    def search_users(search_term):
        """Busca usuarios por nombre, apellido o email"""
        return User.objects.filter(
            Q(name__icontains=search_term) |
            Q(surname__icontains=search_term) |
            Q(email__icontains=search_term)
        )
