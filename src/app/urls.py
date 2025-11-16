from django.urls import path
import app.views as views
from django.contrib.auth import views as auth_views
from app.views.user.user_register_view import UserRegisterView
from app.views.user.user_logout_view import UserLogoutView
from app.views.user.user_profile_view import UserProfileView

from app.views.admin.admin_panel_view import AdminPanelView
from app.views.admin.category.list_category_view import ListCategoryView
from app.views.admin.category.create_category_view import CreateCategoryView
from app.views.admin.category.delete_category_view import DeleteCategoryView

from app.views.admin.product.list_product_view import ListProductView
from app.views.admin.product.create_product_view import CreateProductView
from app.views.admin.product.show_product_view import ShowProductView
from app.views.admin.product.delete_product_view import DeleteProductView

urlpatterns = [
    # Páginas HTML (Template views)
    path('', views.home, name='home'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path("login/", auth_views.LoginView.as_view(template_name="user/login.html", redirect_authenticated_user=True, next_page="/profile" ), name='login'),
    path("logout/", UserLogoutView.as_view(), name='logout'),
    path("register/", UserRegisterView.as_view(), name="register"),

    path("admin/", AdminPanelView.as_view(), name="admin"),

    path('admin/categories/',ListCategoryView.as_view(), name='admin/categories'),
    path('admin/categories/create/',CreateCategoryView.as_view(), name='admin/categories/create'),
    path('admin/categories/delete/<int:category_id>',DeleteCategoryView.as_view(), name='admin/categories/delete'),

    path('admin/products/', ListProductView.as_view(), name='admin/products'),
    path('admin/products/create/', CreateProductView.as_view(), name='admin/products/create'),
    path('admin/products/<int:product_id>/', ShowProductView.as_view(), name='admin/products/show'),
    path('admin/products/delete/<int:product_id>/', DeleteProductView.as_view(), name='admin/products/delete'),


    # CRUD básico
    path('services/', views.list_services, name='list_services'),
    path('services/create/', views.create_service, name='create_service'),
    path('services/<int:service_id>/', views.get_service, name='get_service'),





    path('cash/', views.get_all_quantity, name="get_all_quantity"),
    path('orders/create/', views.create_order, name="create_order"),
    path('orders/', views.get_all_orders, name="get_all_orders"),
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
