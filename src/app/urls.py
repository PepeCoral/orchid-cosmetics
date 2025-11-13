from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Páginas HTML (Template views)
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path("account/login/", auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path("account/logout/", auth_views.LogoutView.as_view(), name='logout'),
    
    # Autenticación API (JSON)
    path('api/auth/register/', views.register, name='api_register'),
    path('api/auth/login/', views.login, name='api_login'),
    path('api/auth/logout/', views.logout, name='api_logout'),
    path('api/auth/check-auth/', views.check_auth, name='check_auth'),
    
    # Perfil de usuario API
    path('api/profile/', views.profile_api, name='profile_api'),
    path('api/profile/update/', views.update_profile, name='update_profile'),
    
    # Gestión de usuarios (solo admin)
    path('api/users/', views.list_users, name='list_users'),
    path('api/users/<int:user_id>/', views.get_user, name='get_user'),
    path('api/users/<int:user_id>/update/', views.update_user, name='update_user'),
    path('api/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('api/users/<int:user_id>/change-role/', views.change_role, name='change_role'),

    # CRUD básico
    path('services/', views.list_services, name='list_services'),
    path('services/create/', views.create_service, name='create_service'),
    path('services/<int:service_id>/', views.get_service, name='get_service'),
    path('services/<int:service_id>/update/', views.update_service, name='update_service'),
    path('services/<int:service_id>/delete/', views.delete_service, name='delete_service'),
    
    # Búsqueda y filtros
    path('services/search/', views.search_services, name='search_services'),
    path('services/category/<int:category_id>/', views.get_services_by_category, name='services_by_category'),
    path('services/department/<str:department>/', views.get_services_by_department, name='services_by_department'),
    path('services/price-range/', views.get_services_by_price_range, name='services_by_price_range'),
    path('services/duration/', views.get_services_by_duration, name='services_by_duration'),
    
    # Ordenamiento
    path('services/sorted/price/', views.get_services_sorted_by_price, name='services_sorted_by_price'),
    path('services/sorted/duration/', views.get_services_sorted_by_duration, name='services_sorted_by_duration'),
    
    # Otros
    path('services/popular/', views.get_popular_services, name='popular_services'),
    path('services/categories-overview/', views.service_categories_overview, name='service_categories_overview'),
]