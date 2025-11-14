from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
import json
from app.models import User
from app.services.user_service import UserService
from app.forms.user_register_form import UserRegisterForm

def home(request):
    return render(request, "home.html")

def profile(request):
    items = User.objects.all()
    return render(request, "profile.html", {'users': items})

def is_admin(user: User):
    """Verifica si el usuario es administrador"""
    return user.is_authenticated and user.is_admin()



@csrf_exempt
@require_http_methods(["POST", "GET"])
def register(request: HttpRequest):
   
    if not request.user.is_anonymous:
        return redirect("/profile")
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            validate_access = UserService.get_user_by_username(username=username)
            if validate_access is not None:
                return render(request, "register.html", {'usernameAlreadyUse': True, "form":form})
            user = UserService.create_user(form.cleaned_data)
            auth_login(request=request,user=user)
            return redirect("/profile",  "register.html",)
        else:
            return render(request,"register.html",context={"form":form})
            
    form = UserRegisterForm() 
    return render(request,template_name="register.html",context={"form":form})


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    email = request.POST.cleaned_data['email']
    password = request.POST.cleaned_data['password']
    user = UserService.authenticate_user(email, password)
    
    auth_login(request, user)


@require_http_methods(["POST", "GET"])
@login_required(login_url="/account/login")
def logout(request):
    auth_logout(request)
    return redirect("/")
   



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