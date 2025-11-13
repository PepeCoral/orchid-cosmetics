from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
import json
from app.models import User
from app.models.user import RoleOptions
from app.services.user_service import UserService

def home(request):
    return render(request, "home.html")

def profile(request):
    items = User.objects.all()
    return render(request, "profile.html", {'users': items})

def is_admin(user):
    """Verifica si el usuario es administrador"""
    return user.is_authenticated and user.role == RoleOptions.ADMIN

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Registro de nuevo usuario"""
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        # Crear usuario
        user = UserService.create_user(data)
        
        # Auto-login después del registro (opcional)
        if request.user.is_authenticated:
            auth_logout(request)
        auth_login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'address': user.address,
                'pay_method': user.pay_method,
                'role': user.role
            }
        }, status=201)
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """Inicio de sesión de usuario"""
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Email y contraseña son requeridos'
            }, status=400)
        
        # Autenticar usuario
        user = UserService.authenticate_user(email, password)
        
        # Realizar login
        auth_login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Login exitoso',
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'address': user.address,
                'pay_method': user.pay_method,
                'role': user.role
            }
        })
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=401)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["POST"])
@login_required
def logout(request):
    """Cerrar sesión"""
    try:
        auth_logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logout exitoso'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def api_home(request):
    """Página de inicio API"""
    return JsonResponse({
        'success': True,
        'message': 'Bienvenido a Orchid Beauty Salon',
        'endpoints': {
            'auth': ['/register/', '/login/', '/logout/', '/profile/'],
            'users': ['/users/', '/users/<id>/', '/users/<id>/update/', '/users/<id>/delete/', '/users/<id>/change-role/'],
            'services': ['/services/', '/services/<id>/', '/services/search/', '/services/category/<id>/']
        }
    })

@require_http_methods(["GET"])
@login_required
def profile_api(request):
    """Obtener perfil del usuario actual"""
    try:
        user = request.user
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'address': user.address,
                'pay_method': user.pay_method,
                'role': user.role,
                'date_joined': user.date_joined.isoformat() if user.date_joined else None,
                'username': user.username
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@login_required
def update_profile(request):
    """Actualizar perfil del usuario actual"""
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        # Actualizar usuario
        updated_user = UserService.update_user(request.user.id, data)
        
        return JsonResponse({
            'success': True,
            'message': 'Perfil actualizado exitosamente',
            'user': {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'address': updated_user.address,
                'pay_method': updated_user.pay_method,
                'role': updated_user.role
            }
        })
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
@login_required
@user_passes_test(is_admin)
def list_users(request):
    """Listar todos los usuarios (solo admin)"""
    try:
        # Opciones de filtrado y búsqueda
        search_term = request.GET.get('search', '')
        role_filter = request.GET.get('role', '')
        
        if search_term:
            users = UserService.search_users(search_term)
        else:
            users = UserService.get_all_users()
        
        # Filtrar por rol si se especifica
        if role_filter:
            users = users.filter(role=role_filter)
        
        users_list = []
        for user in users:
            users_list.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'address': user.address,
                'pay_method': user.pay_method,
                'role': user.role,
                'date_joined': user.date_joined.isoformat() if user.date_joined else None,
                'username': user.username
            })
        
        return JsonResponse({
            'success': True,
            'users': users_list,
            'count': len(users_list),
            'filters': {
                'search': search_term,
                'role': role_filter
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
@login_required
@user_passes_test(is_admin)
def get_user(request, user_id):
    """Obtener usuario específico (solo admin)"""
    try:
        user = UserService.get_user_by_id(user_id)
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'address': user.address,
                'pay_method': user.pay_method,
                'role': user.role,
                'date_joined': user.date_joined.isoformat() if user.date_joined else None,
                'username': user.username
            }
        })
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@login_required
@user_passes_test(is_admin)
def update_user(request, user_id):
    """Actualizar usuario (solo admin)"""
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        # Actualizar usuario
        updated_user = UserService.update_user(user_id, data)
        
        return JsonResponse({
            'success': True,
            'message': 'Usuario actualizado exitosamente',
            'user': {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'address': updated_user.address,
                'pay_method': updated_user.pay_method,
                'role': updated_user.role
            }
        })
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    """Eliminar usuario (solo admin)"""
    try:
        # No permitir eliminarse a sí mismo
        if request.user.id == user_id:
            return JsonResponse({
                'success': False,
                'error': 'No puedes eliminar tu propio usuario'
            }, status=400)
        
        UserService.delete_user(user_id)
        
        return JsonResponse({
            'success': True,
            'message': 'Usuario eliminado exitosamente'
        })
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
@user_passes_test(is_admin)
def change_role(request, user_id):
    """Cambiar rol de usuario (solo admin)"""
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        new_role = data.get('role')
        
        if not new_role:
            return JsonResponse({
                'success': False,
                'error': 'El campo role es requerido'
            }, status=400)
        
        # No permitir cambiar el propio rol
        if request.user.id == user_id:
            return JsonResponse({
                'success': False,
                'error': 'No puedes cambiar tu propio rol'
            }, status=400)
        
        # Cambiar rol
        updated_user = UserService.change_user_role(user_id, new_role)
        
        return JsonResponse({
            'success': True,
            'message': f'Rol cambiado a {new_role} exitosamente',
            'user': {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'role': updated_user.role
            }
        })
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def check_auth(request):
    """Verificar si el usuario está autenticado"""
    return JsonResponse({
        'success': True,
        'authenticated': request.user.is_authenticated,
        'user': {
            'id': request.user.id,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'role': request.user.role
        } if request.user.is_authenticated else None
    })