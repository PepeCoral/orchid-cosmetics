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
    
    # API Home
    path('api/', views.api_home, name='api_home'),
]
