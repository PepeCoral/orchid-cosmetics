from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json
from app.services.service_service import ServiceService


@csrf_exempt
@require_http_methods(["POST"])
def create_service(request):
    """Crear un nuevo servicio"""
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        # Crear servicio
        service = ServiceService.create_service(data)
        
        return JsonResponse({
            'success': True,
            'message': 'Servicio creado exitosamente',
            'service': {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None
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
            'error': f'Error al crear el servicio: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def get_service(request, service_id):
    """Obtener un servicio por ID"""
    try:
        service = ServiceService.get_service_by_id(service_id)
        
        return JsonResponse({
            'success': True,
            'service': {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None,
                'created_at': service.created_at.isoformat() if hasattr(service, 'created_at') else None
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

@require_http_methods(["GET"])
def list_services(request):
    """Listar todos los servicios"""
    try:
        services = ServiceService.get_all_services()
        
        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None
            })
        
        return JsonResponse({
            'success': True,
            'services': services_list,
            'count': len(services_list)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_services_by_category(request, category_id):
    """Obtener servicios por categoría"""
    try:
        services = ServiceService.get_services_by_category(category_id)
        
        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None
            })
        
        return JsonResponse({
            'success': True,
            'services': services_list,
            'count': len(services_list),
            'category_id': category_id
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

@require_http_methods(["GET"])
def get_services_by_department(request, department):
    """Obtener servicios por departamento"""
    try:
        services = ServiceService.get_services_by_department(department)
        
        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None
            })
        
        return JsonResponse({
            'success': True,
            'services': services_list,
            'count': len(services_list),
            'department': department
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_service(request, service_id):
    """Actualizar un servicio existente"""
    try:
        # Obtener datos del request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        # Actualizar servicio
        updated_service = ServiceService.update_service(service_id, data)
        
        return JsonResponse({
            'success': True,
            'message': 'Servicio actualizado exitosamente',
            'service': {
                'id': updated_service.id,
                'name': updated_service.name,
                'description': updated_service.description,
                'price': str(updated_service.price),
                'duration_minutes': updated_service.duration_minutes,
                'department': updated_service.department,
                'image_url': updated_service.image_url,
                'category_id': updated_service.category_id,
                'category_name': updated_service.category.name if updated_service.category else None
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
def delete_service(request, service_id):
    """Eliminar un servicio"""
    try:
        ServiceService.delete_service(service_id)
        
        return JsonResponse({
            'success': True,
            'message': 'Servicio eliminado exitosamente'
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

@require_http_methods(["GET"])
def search_services(request):
    """Buscar servicios por término"""
    try:
        search_term = request.GET.get('q', '')
        
        if not search_term:
            return JsonResponse({
                'success': False,
                'error': 'El parámetro de búsqueda "q" es requerido'
            }, status=400)
        
        services = ServiceService.search_services(search_term)
        
        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None
            })
        
        return JsonResponse({
            'success': True,
            'services': services_list,
            'count': len(services_list),
            'search_term': search_term
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_services_by_price_range(request):
    """Obtener servicios por rango de precios"""
    try:
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
        if not min_price or not max_price:
            return JsonResponse({
                'success': False,
                'error': 'Los parámetros min_price y max_price son requeridos'
            }, status=400)
        
        try:
            min_price_decimal = Decimal(min_price)
            max_price_decimal = Decimal(max_price)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'error': 'Los precios deben ser números válidos'
            }, status=400)
        
        services = ServiceService.get_services_by_price_range(min_price_decimal, max_price_decimal)
        
        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None
            })
        
        return JsonResponse({
            'success': True,
            'services': services_list,
            'count': len(services_list),
            'price_range': {
                'min_price': str(min_price_decimal),
                'max_price': str(max_price_decimal)
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
def get_services_by_duration(request):
    """Obtener servicios por duración máxima"""
    try:
        max_duration = request.GET.get('max_duration')
        
        if not max_duration:
            return JsonResponse({
                'success': False,
                'error': 'El parámetro max_duration es requerido'
            }, status=400)
        
        try:
            max_duration_int = int(max_duration)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'error': 'La duración debe ser un número entero válido'
            }, status=400)
        
        services = ServiceService.get_services_by_duration(max_duration_int)
        
        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None
            })
        
        return JsonResponse({
            'success': True,
            'services': services_list,
            'count': len(services_list),
            'max_duration': max_duration_int
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_popular_services(request):
    """Obtener servicios populares"""
    try:
        limit = request.GET.get('limit', 10)
        
        try:
            limit_int = int(limit)
        except (ValueError, TypeError):
            limit_int = 10
        
        services = ServiceService.get_popular_services(limit_int)
        
        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None
            })
        
        return JsonResponse({
            'success': True,
            'services': services_list,
            'count': len(services_list),
            'limit': limit_int
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_services_sorted_by_price(request):
    """Obtener servicios ordenados por precio"""
    try:
        order = request.GET.get('order', 'asc')
        ascending = order.lower() != 'desc'
        
        services = ServiceService.get_services_sorted_by_price(ascending)
        
        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None
            })
        
        return JsonResponse({
            'success': True,
            'services': services_list,
            'count': len(services_list),
            'order': 'ascending' if ascending else 'descending'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_services_sorted_by_duration(request):
    """Obtener servicios ordenados por duración"""
    try:
        order = request.GET.get('order', 'asc')
        ascending = order.lower() != 'desc'
        
        services = ServiceService.get_services_sorted_by_duration(ascending)
        
        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': str(service.price),
                'duration_minutes': service.duration_minutes,
                'department': service.department,
                'image_url': service.image_url,
                'category_id': service.category_id,
                'category_name': service.category.name if service.category else None
            })
        
        return JsonResponse({
            'success': True,
            'services': services_list,
            'count': len(services_list),
            'order': 'ascending' if ascending else 'descending'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def service_categories_overview(request):
    """Resumen de servicios por categoría"""
    try:
        services_with_category = ServiceService.get_services_with_category()
        services_without_category = ServiceService.get_services_without_category()
        
        with_category_list = []
        for service in services_with_category:
            with_category_list.append({
                'id': service.id,
                'name': service.name,
                'category_name': service.category.name
            })
        
        without_category_list = []
        for service in services_without_category:
            without_category_list.append({
                'id': service.id,
                'name': service.name
            })
        
        return JsonResponse({
            'success': True,
            'with_category': {
                'services': with_category_list,
                'count': len(with_category_list)
            },
            'without_category': {
                'services': without_category_list,
                'count': len(without_category_list)
            },
            'total_services': len(with_category_list) + len(without_category_list)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)