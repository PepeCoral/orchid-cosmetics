from django.urls import path
import app.views as views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Páginas HTML (Template views)
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", next_page="/profile"), name='login'),
    # path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path("register/", views.user_controller.register, name="register"),
    

    # CRUD básico
    path('services/', views.list_services, name='list_services'),
    path('services/create/', views.create_service, name='create_service'),
    path('services/<int:service_id>/', views.get_service, name='get_service'),

    path('products/', views.list_products, name='list_products'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:product_id>/', views.get_service, name='get_product'),
]