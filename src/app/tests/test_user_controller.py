import pytest
import json
from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock
from app.models import User, RoleOptions
from app.views import *
from app.services import UserService
from src.app.views.user_controller import api_home, change_role, check_auth, delete_user, get_user, home, is_admin, list_users, login, logout, profile, profile_api, register, update_profile, update_user

User = get_user_model()

@pytest.mark.django_db
class TestViewController:

    def setup_method(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_home_view(self):
        """Test para la vista home"""
        request = self.factory.get('/')
        response = home(request)
        
        assert response.status_code == 200
        assert 'home.html' in response.template_name

    def test_profile_view(self):
        """Test para la vista profile"""
        # Crear algunos usuarios de prueba
        User.objects.create_user(
            username='user1@test.com',
            email='user1@test.com',
            password='password123',
            first_name='User1'
        )
        User.objects.create_user(
            username='user2@test.com',
            email='user2@test.com',
            password='password123',
            first_name='User2'
        )
        
        request = self.factory.get('/profile/')
        response = profile(request)
        
        assert response.status_code == 200
        assert 'profile.html' in response.template_name
        assert 'users' in response.context_data
        assert response.context_data['users'].count() == 2

    def test_is_admin_function(self):
        """Test para la función is_admin"""
        # Crear usuario admin
        admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='password123',
            first_name='Admin',
            role=RoleOptions.ADMIN
        )
        
        # Crear usuario regular
        regular_user = User.objects.create_user(
            username='user@test.com',
            email='user@test.com',
            password='password123',
            first_name='User',
            role=RoleOptions.USER
        )
        
        # Crear usuario anónimo
        anonymous_user = AnonymousUser()
        
        assert is_admin(admin_user) == True
        assert is_admin(regular_user) == False
        assert is_admin(anonymous_user) == False

    @patch('app.views.UserService.create_user')
    @patch('app.views.auth_login')
    @patch('app.views.auth_logout')
    def test_register_success(self, mock_logout, mock_login, mock_create_user):
        """Test de registro exitoso"""
        # Mock del usuario creado
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.first_name = 'John'
        mock_user.last_name = 'Doe'
        mock_user.email = 'john@example.com'
        mock_user.address = ''
        mock_user.pay_method = ''
        mock_user.role = RoleOptions.USER
        mock_create_user.return_value = mock_user
        
        # Request con datos JSON
        data = {
            'email': 'john@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        request = self.factory.post(
            '/register/',
            data=json.dumps(data),
            content_type='application/json'
        )
        request.user = AnonymousUser()
        
        response = register(request)
        
        assert response.status_code == 201
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['message'] == 'Usuario registrado exitosamente'
        mock_create_user.assert_called_once_with(data)

    @patch('app.views.UserService.create_user')
    def test_register_validation_error(self, mock_create_user):
        """Test de registro con error de validación"""
        mock_create_user.side_effect = ValidationError("Email inválido")
        
        data = {
            'email': 'invalid-email',
            'password': '123',
            'first_name': 'John'
        }
        
        request = self.factory.post(
            '/register/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        response = register(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'error' in response_data

    @patch('app.views.UserService.authenticate_user')
    @patch('app.views.auth_login')
    def test_login_success(self, mock_login, mock_authenticate):
        """Test de login exitoso"""
        # Mock del usuario autenticado
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.first_name = 'John'
        mock_user.last_name = 'Doe'
        mock_user.email = 'john@example.com'
        mock_user.address = '123 Main St'
        mock_user.pay_method = 'Credit Card'
        mock_user.role = RoleOptions.USER
        mock_authenticate.return_value = mock_user
        
        data = {
            'email': 'john@example.com',
            'password': 'password123'
        }
        
        request = self.factory.post(
            '/login/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        response = login(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['message'] == 'Login exitoso'
        mock_authenticate.assert_called_once_with('john@example.com', 'password123')
        mock_login.assert_called_once_with(request, mock_user)

    def test_login_missing_credentials(self):
        """Test de login sin credenciales"""
        data = {
            'email': '',
            'password': ''
        }
        
        request = self.factory.post(
            '/login/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        response = login(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'Email y contraseña son requeridos' in response_data['error']

    @patch('app.views.UserService.authenticate_user')
    def test_login_invalid_credentials(self, mock_authenticate):
        """Test de login con credenciales inválidas"""
        mock_authenticate.side_effect = ValidationError("Credenciales inválidas")
        
        data = {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        }
        
        request = self.factory.post(
            '/login/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        response = login(request)
        
        assert response.status_code == 401
        response_data = json.loads(response.content)
        assert response_data['success'] == False

    @patch('app.views.auth_logout')
    def test_logout_success(self, mock_logout):
        """Test de logout exitoso"""
        # Crear y autenticar usuario
        user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='password123',
            first_name='Test'
        )
        
        request = self.factory.post('/logout/')
        request.user = user
        
        response = logout(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['message'] == 'Logout exitoso'
        mock_logout.assert_called_once_with(request)

    def test_api_home(self):
        """Test para la vista api_home"""
        request = self.factory.get('/api/')
        response = api_home(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert 'endpoints' in response_data

    def test_profile_api_authenticated(self):
        """Test para profile_api con usuario autenticado"""
        user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            address='123 Main St',
            pay_method='Credit Card',
            role=RoleOptions.USER
        )
        
        request = self.factory.get('/api/profile/')
        request.user = user
        
        response = profile_api(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['user']['first_name'] == 'John'
        assert response_data['user']['email'] == 'test@example.com'

    def test_profile_api_unauthenticated(self):
        """Test para profile_api sin autenticar (debería redirigir)"""
        request = self.factory.get('/api/profile/')
        request.user = AnonymousUser()
        
        response = profile_api(request)
        
        # Debería redirigir al login
        assert response.status_code == 302

    @patch('app.views.UserService.update_user')
    def test_update_profile_success(self, mock_update_user):
        """Test de actualización de perfil exitosa"""
        user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='password123',
            first_name='Original'
        )
        
        # Mock del usuario actualizado
        updated_user = MagicMock()
        updated_user.id = 1
        updated_user.first_name = 'Updated'
        updated_user.last_name = 'Name'
        updated_user.email = 'test@example.com'
        updated_user.address = 'New Address'
        updated_user.pay_method = 'PayPal'
        updated_user.role = RoleOptions.USER
        mock_update_user.return_value = updated_user
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'address': 'New Address',
            'pay_method': 'PayPal'
        }
        
        request = self.factory.patch(
            '/api/profile/update/',
            data=json.dumps(data),
            content_type='application/json'
        )
        request.user = user
        
        response = update_profile(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['user']['first_name'] == 'Updated'

    @patch('app.views.UserService.update_user')
    def test_update_profile_validation_error(self, mock_update_user):
        """Test de actualización de perfil con error"""
        user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='password123',
            first_name='Test'
        )
        
        mock_update_user.side_effect = ValidationError("Email ya en uso")
        
        data = {'email': 'existing@example.com'}
        
        request = self.factory.patch(
            '/api/profile/update/',
            data=json.dumps(data),
            content_type='application/json'
        )
        request.user = user
        
        response = update_profile(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False

    @patch('app.views.UserService.get_all_users')
    def test_list_users_admin(self, mock_get_all_users):
        """Test de list_users para administrador"""
        # Crear usuario admin
        admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='password123',
            first_name='Admin',
            role=RoleOptions.ADMIN
        )
        
        # Mock de usuarios retornados
        mock_users = [
            MagicMock(
                id=1,
                first_name='User1',
                last_name='Test',
                email='user1@test.com',
                address='',
                pay_method='',
                role=RoleOptions.USER,
                date_joined=MagicMock(isoformat=lambda: '2023-01-01T00:00:00'),
                username='user1@test.com'
            ),
            MagicMock(
                id=2,
                first_name='User2',
                last_name='Test',
                email='user2@test.com',
                address='',
                pay_method='',
                role=RoleOptions.ADMIN,
                date_joined=MagicMock(isoformat=lambda: '2023-01-02T00:00:00'),
                username='user2@test.com'
            )
        ]
        mock_get_all_users.return_value = mock_users
        
        request = self.factory.get('/api/users/')
        request.user = admin_user
        
        response = list_users(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert len(response_data['users']) == 2

    def test_list_users_non_admin(self):
        """Test de list_users para usuario no administrador"""
        # Crear usuario regular
        regular_user = User.objects.create_user(
            username='user@test.com',
            email='user@test.com',
            password='password123',
            first_name='User',
            role=RoleOptions.USER
        )
        
        request = self.factory.get('/api/users/')
        request.user = regular_user
        
        response = list_users(request)
        
        # Debería redirigir o denegar acceso
        assert response.status_code in [302, 403]

    @patch('app.views.UserService.get_user_by_id')
    def test_get_user_success(self, mock_get_user):
        """Test de obtención de usuario específico"""
        admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='password123',
            first_name='Admin',
            role=RoleOptions.ADMIN
        )
        
        # Mock del usuario buscado
        target_user = MagicMock()
        target_user.id = 2
        target_user.first_name = 'Target'
        target_user.last_name = 'User'
        target_user.email = 'target@test.com'
        target_user.address = '123 St'
        target_user.pay_method = 'Card'
        target_user.role = RoleOptions.USER
        target_user.date_joined = MagicMock(isoformat=lambda: '2023-01-01T00:00:00')
        target_user.username = 'target@test.com'
        mock_get_user.return_value = target_user
        
        request = self.factory.get('/api/users/2/')
        request.user = admin_user
        
        response = get_user(request, 2)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['user']['first_name'] == 'Target'

    @patch('app.views.UserService.update_user')
    def test_update_user_admin_success(self, mock_update_user):
        """Test de actualización de usuario por admin"""
        admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='password123',
            first_name='Admin',
            role=RoleOptions.ADMIN
        )
        
        updated_user = MagicMock()
        updated_user.id = 2
        updated_user.first_name = 'Updated'
        updated_user.last_name = 'User'
        updated_user.email = 'updated@test.com'
        updated_user.address = 'New Address'
        updated_user.pay_method = 'New Method'
        updated_user.role = RoleOptions.USER
        mock_update_user.return_value = updated_user
        
        data = {
            'first_name': 'Updated',
            'address': 'New Address',
            'pay_method': 'New Method'
        }
        
        request = self.factory.patch(
            '/api/users/2/update/',
            data=json.dumps(data),
            content_type='application/json'
        )
        request.user = admin_user
        
        response = update_user(request, 2)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['user']['first_name'] == 'Updated'

    @patch('app.views.UserService.delete_user')
    def test_delete_user_success(self, mock_delete_user):
        """Test de eliminación de usuario exitosa"""
        admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='password123',
            first_name='Admin',
            role=RoleOptions.ADMIN
        )
        
        mock_delete_user.return_value = True
        
        request = self.factory.delete('/api/users/2/delete/')
        request.user = admin_user
        
        response = delete_user(request, 2)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        mock_delete_user.assert_called_once_with(2)

    def test_delete_user_self(self):
        """Test que evita que un admin se elimine a sí mismo"""
        admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='password123',
            first_name='Admin',
            role=RoleOptions.ADMIN
        )
        
        request = self.factory.delete('/api/users/1/delete/')
        request.user = admin_user
        
        response = delete_user(request, 1)  # Mismo ID del usuario
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'No puedes eliminar tu propio usuario' in response_data['error']

    @patch('app.views.UserService.change_user_role')
    def test_change_role_success(self, mock_change_role):
        """Test de cambio de rol exitoso"""
        admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='password123',
            first_name='Admin',
            role=RoleOptions.ADMIN
        )
        
        updated_user = MagicMock()
        updated_user.id = 2
        updated_user.first_name = 'User'
        updated_user.last_name = 'Test'
        updated_user.email = 'user@test.com'
        updated_user.role = RoleOptions.ADMIN
        mock_change_role.return_value = updated_user
        
        data = {'role': RoleOptions.ADMIN}
        
        request = self.factory.post(
            '/api/users/2/change-role/',
            data=json.dumps(data),
            content_type='application/json'
        )
        request.user = admin_user
        
        response = change_role(request, 2)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['success'] == True
        assert response_data['user']['role'] == RoleOptions.ADMIN

    def test_change_role_self(self):
        """Test que evita que un admin cambie su propio rol"""
        admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='password123',
            first_name='Admin',
            role=RoleOptions.ADMIN
        )
        
        data = {'role': RoleOptions.USER}
        
        request = self.factory.post(
            '/api/users/1/change-role/',
            data=json.dumps(data),
            content_type='application/json'
        )
        request.user = admin_user
        
        response = change_role(request, 1)  # Mismo ID del usuario
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'No puedes cambiar tu propio rol' in response_data['error']

    def test_change_role_missing_role(self):
        """Test de cambio de rol sin especificar rol"""
        admin_user = User.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='password123',
            first_name='Admin',
            role=RoleOptions.ADMIN
        )
        
        data = {}  # Sin campo role
        
        request = self.factory.post(
            '/api/users/2/change-role/',
            data=json.dumps(data),
            content_type='application/json'
        )
        request.user = admin_user
        
        response = change_role(request, 2)
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data['success'] == False
        assert 'El campo role es requerido' in response_data['error']

    def test_check_auth_authenticated(self):
        """Test de check_auth con usuario autenticado"""
        user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            role=RoleOptions.USER
        )
        
        request = self.factory.get('/check-auth/')
        request.user = user
        
        response = check_auth(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['authenticated'] == True
        assert response_data['user']['first_name'] == 'John'

    def test_check_auth_unauthenticated(self):
        """Test de check_auth sin usuario autenticado"""
        request = self.factory.get('/check-auth/')
        request.user = AnonymousUser()
        
        response = check_auth(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data['authenticated'] == False
        assert response_data['user'] is None

    # Tests para métodos HTTP no permitidos
    def test_register_wrong_method(self):
        """Test de registro con método HTTP incorrecto"""
        request = self.factory.get('/register/')
        response = register(request)
        assert response.status_code == 405  # Method Not Allowed

    def test_login_wrong_method(self):
        """Test de login con método HTTP incorrecto"""
        request = self.factory.get('/login/')
        response = login(request)
        assert response.status_code == 405

    def test_logout_wrong_method(self):
        """Test de logout con método HTTP incorrecto"""
        user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='password123',
            first_name='Test'
        )
        
        request = self.factory.get('/logout/')
        request.user = user
        response = logout(request)
        assert response.status_code == 405