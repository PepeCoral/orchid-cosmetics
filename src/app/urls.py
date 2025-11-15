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
    path('products/<int:product_id>/', views.get_product, name='get_product'),

    path('categories/',views.list_categories, name='list_categories'),
    path('categories/create/',views.create_category, name='create_category'),
    
    path('cash/', views.get_all_quantity, name="get_all_quantity")
    # path('services/<int:service_id>/update/', views.update_service, name='update_service'),
    # path('services/<int:service_id>/delete/', views.delete_service, name='delete_service'),
    
    # # Búsqueda y filtros
    # path('services/search/', views.search_services, name='search_services'),
    # path('services/category/<int:category_id>/', views.get_services_by_category, name='services_by_category'),
    # path('services/department/<str:department>/', views.get_services_by_department, name='services_by_department'),
    # path('services/price-range/', views.get_services_by_price_range, name='services_by_price_range'),
    # path('services/duration/', views.get_services_by_duration, name='services_by_duration'),
    
    # # Ordenamiento
    # path('services/sorted/price/', views.get_services_sorted_by_price, name='services_sorted_by_price'),
    # path('services/sorted/duration/', views.get_services_sorted_by_duration, name='services_sorted_by_duration'),
    
    # # Otros
    # path('services/popular/', views.get_popular_services, name='popular_services'),
    # path('services/categories-overview/', views.service_categories_overview, name='service_categories_overview'),
]