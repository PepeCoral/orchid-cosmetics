from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from unittest.mock import patch, MagicMock

from django.test import TestCase
from app.models.user import User, RoleOptions
from app.services.user_service import UserService


class TestUserService(TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'pay_method': 'Credit Card',
            'role': RoleOptions.USER
        }
        self.admin_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'admin',
            'last_name': 'admin',
            'address': '123 Main St',
            'pay_method': 'Credit Card',
            'role': RoleOptions.ADMIN
        }
        self.update_data = {
            'username':'Updated',
            'email':'updated@gmail.com',
            'password':'passwordUpdated',
            'first_name': 'Updated',
            'last_name': 'LastName',
            'address': 'New Address',
            'pay_method': 'PayPal',
            'role':RoleOptions.ADMIN
        }

    def test_create_user_success(self):
        """Test de creación exitosa de usuario"""
        test_data = self.user_data.copy()
        user = self.user_service.create_user(test_data)
        
        assert user.email == test_data['email']
        assert user.first_name == test_data['first_name']
        assert user.last_name == test_data['last_name']
        assert user.address == test_data['address']
        assert user.pay_method == test_data['pay_method']
        assert user.role == test_data['role']
        assert user.username == test_data['username']

    def test_create_invalid_data(self):
        """Test que rechaza emails inválidos"""
        test_data = self.user_data.copy()
        
        self.user_service.create_user(test_data)
        
        with self.assertRaises(ValidationError, msg="Username already in use"):
            self.user_service.create_user(test_data)
        with self.assertRaises(ValidationError, msg="Email already in use"):
            test_data['username']='otro'
            self.user_service.create_user(test_data)
        with self.assertRaises(ValidationError, msg="Passwords do not match"):
            test_data['email']='otro@gmail.com'
            test_data['password']='diferente'
            self.user_service.create_user(test_data)


    def test_get_user_by_id(self):
        test_data = self.user_data.copy()
        user = self.user_service.create_user(test_data)

        test_user = self.user_service.get_user_by_id(user.id)
        self.assertIsNotNone(test_user,user)

    
    def test_get_user_by_id_not_found(self):
        """Test de obtención de usuario por ID inexistente"""
        with self.assertRaises(ValidationError, msg="Usuario no encontrado"):
            UserService.get_user_by_id(999)  # ID que no existe

    
    def test_update_user_success(self):
        """Test de actualización exitosa de usuario"""
        user_data = self.user_data.copy()
        
        user = self.user_service.create_user(user_data)
        
        update_data = self.update_data.copy()
        
        updated_user = self.user_service.update_user(user.id, update_data)
    
        assert updated_user.username == 'Updated'
        assert updated_user.email == 'updated@gmail.com'
        assert updated_user.check_password('passwordUpdated')
        assert updated_user.first_name == 'Updated'
        assert updated_user.last_name == 'LastName'
        assert updated_user.address == 'New Address'
        assert updated_user.pay_method == 'PayPal'
        assert updated_user.role == RoleOptions.ADMIN

    def test_update_user_duplicate_information(self):
        """Test que evita actualizar a un email ya existente"""
        # Crear primer usuario
        user_data = self.user_data.copy()
        self.user_service.create_user(user_data)
        
        # Crear segundo usuario
        user_data['username']='otro'
        user_data['email']='other@email.com'
        user2 = self.user_service.create_user(user_data)
        
        # Intentar cambiar email del usuario2 al email del usuario1
        with self.assertRaises(ValidationError, msg="Username already in use"):
            self.user_service.update_user(user2.id, {'username': 'testuser'})
        with self.assertRaises(ValidationError, msg="Email already in use"):
            self.user_service.update_user(user2.id, {'email': 'test@example.com'})


    def test_update_user_password(self):
        """Test de actualización de contraseña"""
        user_data = self.user_data.copy()
        
        user = self.user_service.create_user(user_data)
        
        update_data = {'password': 'newpassword123', 'confirm_password': 'newpassword123'}
        updated_user = self.user_service.update_user(user.id, update_data)
        
        # Verificar que la nueva contraseña funciona
        assert updated_user.check_password('newpassword123')

    def test_update_user_not_found(self):
        """Test de actualización de usuario inexistente"""
        with self.assertRaises(ValidationError, msg="Usuario no encontrado"):
            self.user_service.update_user(999, {'first_name': 'Updated'})

    def test_delete_user_success(self):
        """Test de eliminación exitosa de usuario"""
        user_data = self.user_data.copy()
        
        user = self.user_service.create_user(user_data)
        
        result = self.user_service.delete_user(user.id)
        
        assert result == True
        # Verificar que el usuario ya no existe
        with self.assertRaises(ValidationError, msg="Usuario no encontrado"):
            self.user_service.get_user_by_id(user.id)

    def test_get_all_users(self):
        """Test de obtención de todos los usuarios"""
        # Crear varios usuarios
        users_data = [
            {'username': f'user{i}', 'email': f'user{i}@example.com', 'password': 'password123', 'confirm_password': 'password123', 'first_name': f'User{i}'}
            for i in range(3)
        ]
        
        created_users = []
        for data in users_data:
            created_users.append(self.user_service.create_user(data))
        
        all_users = self.user_service.get_all_users()
        
        assert all_users.count() == 3
        for user in created_users:
            assert user in all_users

    def test_change_user_role_success(self):
        """Test de cambio de rol exitoso"""
        user_data = {
            'username': 'changerole',
            'email': 'changerole@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'ChangeRole',
            'role': RoleOptions.USER
        }
        
        user = self.user_service.create_user(user_data)
        assert user.role == RoleOptions.USER
        
        updated_user = self.user_service.change_user_role(user.id, RoleOptions.ADMIN)
        assert updated_user.role == RoleOptions.ADMIN

    def test_change_user_role_invalid_role(self):
        """Test de cambio a rol inválido"""
        user_data = {
            'username': 'invalidrole',
            'email': 'invalidrole@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'InvalidRole'
        }
        
        user = self.user_service.create_user(user_data)
        
        with self.assertRaises(ValidationError, msg="Rol inválido"):
            self.user_service.change_user_role(user.id, 'INVALID_ROLE')

    def test_change_user_role_user_not_found(self):
        """Test de cambio de rol en usuario inexistente"""
        with self.assertRaises(ValidationError, msg="Usuario no encontrado"):
            self.user_service.change_user_role(999, RoleOptions.ADMIN)

    def test_search_users(self):
        """Test de búsqueda de usuarios"""
        # Crear usuarios de prueba
        users_data = [
            {'email': 'john@example.com', 'password': 'pass123','confirm_password': 'pass123', 'first_name': 'John', 'last_name': 'Smith'},
            {'email': 'jane@example.com', 'password': 'pass123', 'confirm_password': 'pass123', 'first_name': 'Jane', 'last_name': 'Doe'},
            {'email': 'bob@example.com', 'password': 'pass123', 'confirm_password': 'pass123', 'first_name': 'Bob', 'last_name': 'Johnson'},
        ]
        
        for data in users_data:
            self.user_service.create_user(data)
        
        # Buscar por first_name
        results = self.user_service.search_users('John')
        assert results.count() == 1
        assert results.first().first_name == 'John'
        
        # Buscar por last_name
        results = self.user_service.search_users('Doe')
        assert results.count() == 1
        assert results.first().last_name == 'Doe'
        
        # Buscar por email
        results = self.user_service.search_users('jane@example.com')
        assert results.count() == 1
        assert results.first().email == 'jane@example.com'
        
        # Búsqueda que no encuentra resultados
        results = self.user_service.search_users('Nonexistent')
        assert results.count() == 0

    def test_get_admin_users(self):
        """Test de obtención de usuarios administradores"""
        # Crear usuarios con diferentes roles
        user_data = self.user_data.copy()
        admin_data = self.admin_data.copy()

        self.user_service.create_user(admin_data)
        self.user_service.create_user(user_data)
        
        admin_users = self.user_service.get_admin_users()
        assert admin_users.count() == 1
        assert admin_users.first().role == RoleOptions.ADMIN

    def test_get_regular_users(self):
        """Test de obtención de usuarios regulares"""
        # Crear usuarios con diferentes roles
        user_data = self.user_data.copy()
        admin_data = self.admin_data.copy()
        
        self.user_service.create_user(admin_data)
        self.user_service.create_user(user_data)
        
        regular_users = self.user_service.get_regular_users()
        assert regular_users.count() == 1
        assert regular_users.first().role == RoleOptions.USER

    def test_promote_to_admin(self):
        """Test de promoción a administrador"""
        user_data = self.user_data.copy()
        
        user = self.user_service.create_user(user_data)
        promoted_user = self.user_service.promote_to_admin(user.id)
        
        assert promoted_user.role == RoleOptions.ADMIN

    def test_demote_to_user(self):
        """Test de degradación a usuario regular"""
        admin_data = self.admin_data.copy()
        
        admin = self.user_service.create_user(admin_data)
        demoted_user = self.user_service.demote_to_user(admin.id)
        
        assert demoted_user.role == RoleOptions.USER