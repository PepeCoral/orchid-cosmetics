from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from unittest.mock import patch, MagicMock

from django.test import TestCase
from app.models.user import User, RoleOptions
from app.services import UserService


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

    def test_validate_email_success(self):
        """Test que valida emails correctos"""
        valid_emails = [
            'test@example.com',
            'user.name@domain.co',
            'user+tag@example.org',
            'test123@test.com'
        ]
        
        for email in valid_emails:
            assert UserService.validate_email(email) == True

    def test_validate_email_invalid(self):
        """Test que rechaza emails inválidos"""
        invalid_emails = [
            'invalid-email',
            'user@',
            '@domain.com',
            'user@domain',
            'user@.com'
        ]
        
        for email in invalid_emails:
            with self.assertRaises(ValidationError, msg="Formato de email inválido"):
                UserService.validate_email(email)

    def test_validate_password_success(self):
        """Test que valida contraseñas correctas"""
        valid_passwords = ['123456', 'password123', 'securepass']
        
        for password in valid_passwords:
            assert UserService.validate_password(password, password) == True

    def test_validate_password_too_short(self):
        """Test que rechaza contraseñas muy cortas"""
        short_passwords = ['12345', 'abc', 'p', '']
        
        for password in short_passwords:
            with self.assertRaises(ValidationError, msg="La contraseña debe tener al menos 6 caracteres"):
                UserService.validate_password(password, password)

    def test_validate_password_mismatch(self):
        password = 'password123'
        confirm_password = 'password124'
        with self.assertRaises(ValidationError, msg="Las contraseñas no coinciden"):
            UserService.validate_password(password, confirm_password)

    def test_create_user_success(self):
        """Test de creación exitosa de usuario"""
        user_data = self.user_data.copy()
        user = UserService.create_user(user_data)
        
        assert user.email == user_data['email']
        assert user.first_name == user_data['first_name']
        assert user.last_name == user_data['last_name']
        assert user.address == user_data['address']
        assert user.pay_method == user_data['pay_method']
        assert user.role == user_data['role']
        assert user.username == user_data['email']  # username debe ser igual al email
        assert user.check_password(user_data['password'])  # Verificar que la contraseña se hasheó

    def test_create_user_duplicate_email(self):
        """Test que evita crear usuarios con email duplicado"""
        user_data = self.user_data.copy()
        # Crear primer usuario
        UserService.create_user(user_data)
        
        # Intentar crear segundo usuario con mismo email
        with self.assertRaises(ValidationError, msg="El email ya está registrado"):
            UserService.create_user(user_data)

    def test_create_user_invalid_email(self):
        """Test que valida email al crear usuario"""
        user_data = {
            'email': 'invalid-email',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'John'
        }
        
        with self.assertRaises(ValidationError, msg="Formato de email inválido"):
            UserService.create_user(user_data)

    def test_create_user_short_password(self):
        """Test que valida longitud de contraseña al crear usuario"""
        user_data = {
            'email': 'test@example.com',
            'password': '123',
            'confirm_password': '123',
            'first_name': 'John'
        }
        
        with self.assertRaises(ValidationError, msg="La contraseña debe tener al menos 6 caracteres"):
            UserService.create_user(user_data)

    def test_create_user_default_values(self):
        """Test que verifica valores por defecto"""
        user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'John'
        }
        
        user = UserService.create_user(user_data)
        
        assert user.last_name == ''
        assert user.address == ''
        assert user.pay_method == ''
        assert user.role == RoleOptions.USER

    def test_authenticate_user_success(self):
        """Test de autenticación exitosa"""
        user_data = {
            'username': 'authuser',
            'email': 'auth@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'Auth'
        }
        
        user = UserService.create_user(user_data)
        
        # Mock de authenticate para retornar el usuario
        with patch('app.services.UserService.authenticate') as mock_authenticate:
            mock_authenticate.return_value = user
            authenticated_user = UserService.authenticate_user(
                user_data['username'], 
                user_data['password']
            )
            
            assert authenticated_user == user

    def test_authenticate_user_invalid_credentials(self):
        """Test de autenticación con credenciales inválidas"""
        with patch('app.services.UserService.authenticate') as mock_authenticate:
            mock_authenticate.return_value = None
            
            with self.assertRaises(ValidationError, msg="Credenciales inválidas"):
                UserService.authenticate_user('wronguser', 'wrongpass')

    def test_get_user_by_id_success(self):
        """Test de obtención de usuario por ID"""
        user_data = self.user_data.copy()
        
        created_user = UserService.create_user(user_data)
        found_user = UserService.get_user_by_id(created_user.id)
        
        assert found_user == created_user

    def test_get_user_by_id_not_found(self):
        """Test de obtención de usuario por ID inexistente"""
        with self.assertRaises(ValidationError, msg="Usuario no encontrado"):
            UserService.get_user_by_id(999)  # ID que no existe

    def test_get_user_by_email_success(self):
        """Test de obtención de usuario por email"""
        user_data = self.user_data.copy()
        
        created_user = UserService.create_user(user_data)
        found_user = UserService.get_user_by_email(user_data['email'])
        
        assert found_user == created_user

    def test_get_user_by_email_not_found(self):
        """Test de obtención de usuario por email inexistente"""
        with self.assertRaises(ValidationError, msg="Usuario no encontrado"):
            UserService.get_user_by_email('nonexistent@example.com')

    def test_update_user_success(self):
        """Test de actualización exitosa de usuario"""
        user_data = self.user_data.copy()
        
        user = UserService.create_user(user_data)
        
        update_data = {
            'first_name': 'Updated',
            'last_name': 'LastName',
            'address': 'New Address',
            'pay_method': 'PayPal'
        }
        
        updated_user = UserService.update_user(user.id, update_data)
        
        assert updated_user.first_name == 'Updated'
        assert updated_user.last_name == 'LastName'
        assert updated_user.address == 'New Address'
        assert updated_user.pay_method == 'PayPal'

    def test_update_user_email(self):
        """Test de actualización de email"""
        user_data = {
            'email': 'old@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'Test'
        }
        
        user = UserService.create_user(user_data)
        
        update_data = {'email': 'new@example.com'}
        updated_user = UserService.update_user(user.id, update_data)
        
        assert updated_user.email == 'new@example.com'
        assert updated_user.username == 'new@example.com'  # username también debe actualizarse

    def test_update_user_duplicate_email(self):
        """Test que evita actualizar a un email ya existente"""
        # Crear primer usuario
        user1_data = {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'User1'
        }
        user1 = UserService.create_user(user1_data)
        
        # Crear segundo usuario
        user2_data = {
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'User2'
        }
        user2 = UserService.create_user(user2_data)
        
        # Intentar cambiar email del usuario2 al email del usuario1
        with self.assertRaises(ValidationError, msg="El email ya está en uso"):
            UserService.update_user(user2.id, {'email': 'user1@example.com'})

    def test_update_user_password(self):
        """Test de actualización de contraseña"""
        user_data = self.user_data.copy()
        
        user = UserService.create_user(user_data)
        
        update_data = {'password': 'newpassword123', 'confirm_password': 'newpassword123'}
        updated_user = UserService.update_user(user.id, update_data)
        
        # Verificar que la nueva contraseña funciona
        assert updated_user.check_password('newpassword123')

    def test_update_user_not_found(self):
        """Test de actualización de usuario inexistente"""
        with self.assertRaises(ValidationError, msg="Usuario no encontrado"):
            UserService.update_user(999, {'first_name': 'Updated'})

    def test_delete_user_success(self):
        """Test de eliminación exitosa de usuario"""
        user_data = self.user_data.copy()
        
        user = UserService.create_user(user_data)
        
        result = UserService.delete_user(user.id)
        
        assert result == True
        # Verificar que el usuario ya no existe
        with self.assertRaises(ValidationError, msg="Usuario no encontrado"):
            UserService.get_user_by_id(user.id)

    def test_get_all_users(self):
        """Test de obtención de todos los usuarios"""
        # Crear varios usuarios
        users_data = [
            {'username': f'user{i}', 'email': f'user{i}@example.com', 'password': 'password123', 'confirm_password': 'password123', 'first_name': f'User{i}'}
            for i in range(3)
        ]
        
        created_users = []
        for data in users_data:
            created_users.append(UserService.create_user(data))
        
        all_users = UserService.get_all_users()
        
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
        
        user = UserService.create_user(user_data)
        assert user.role == RoleOptions.USER
        
        updated_user = UserService.change_user_role(user.id, RoleOptions.ADMIN)
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
        
        user = UserService.create_user(user_data)
        
        with self.assertRaises(ValidationError, msg="Rol inválido"):
            UserService.change_user_role(user.id, 'INVALID_ROLE')

    def test_change_user_role_user_not_found(self):
        """Test de cambio de rol en usuario inexistente"""
        with self.assertRaises(ValidationError, msg="Usuario no encontrado"):
            UserService.change_user_role(999, RoleOptions.ADMIN)

    def test_search_users(self):
        """Test de búsqueda de usuarios"""
        # Crear usuarios de prueba
        users_data = [
            {'email': 'john@example.com', 'password': 'pass123','confirm_password': 'pass123', 'first_name': 'John', 'last_name': 'Smith'},
            {'email': 'jane@example.com', 'password': 'pass123', 'confirm_password': 'pass123', 'first_name': 'Jane', 'last_name': 'Doe'},
            {'email': 'bob@example.com', 'password': 'pass123', 'confirm_password': 'pass123', 'first_name': 'Bob', 'last_name': 'Johnson'},
        ]
        
        for data in users_data:
            UserService.create_user(data)
        
        # Buscar por first_name
        results = UserService.search_users('John')
        assert results.count() == 1
        assert results.first().first_name == 'John'
        
        # Buscar por last_name
        results = UserService.search_users('Doe')
        assert results.count() == 1
        assert results.first().last_name == 'Doe'
        
        # Buscar por email
        results = UserService.search_users('jane@example.com')
        assert results.count() == 1
        assert results.first().email == 'jane@example.com'
        
        # Búsqueda que no encuentra resultados
        results = UserService.search_users('Nonexistent')
        assert results.count() == 0

    def test_get_admin_users(self):
        """Test de obtención de usuarios administradores"""
        # Crear usuarios con diferentes roles
        user_data = self.user_data.copy()
        admin_data = self.admin_data.copy()

        UserService.create_user(admin_data)
        UserService.create_user(user_data)
        
        admin_users = UserService.get_admin_users()
        assert admin_users.count() == 1
        assert admin_users.first().role == RoleOptions.ADMIN

    def test_get_regular_users(self):
        """Test de obtención de usuarios regulares"""
        # Crear usuarios con diferentes roles
        user_data = self.user_data.copy()
        admin_data = self.admin_data.copy()
        
        UserService.create_user(admin_data)
        UserService.create_user(user_data)
        
        regular_users = UserService.get_regular_users()
        assert regular_users.count() == 1
        assert regular_users.first().role == RoleOptions.USER

    def test_promote_to_admin(self):
        """Test de promoción a administrador"""
        user_data = self.user_data.copy()
        
        user = UserService.create_user(user_data)
        promoted_user = UserService.promote_to_admin(user.id)
        
        assert promoted_user.role == RoleOptions.ADMIN

    def test_demote_to_user(self):
        """Test de degradación a usuario regular"""
        admin_data = self.admin_data.copy()
        
        admin = UserService.create_user(admin_data)
        demoted_user = UserService.demote_to_user(admin.id)
        
        assert demoted_user.role == RoleOptions.USER