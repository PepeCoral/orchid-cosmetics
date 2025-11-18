from django.urls import path
import app.views as views
from django.contrib.auth import views as auth_views

from app.views.admin.category.update_category_view import UpdateCategoryView
from app.views.home_view import HomeView
from app.views.user.user_delete_view import DeleteUserView
from app.views.static_pages import ContactView
from app.views.user.user_register_view import UserRegisterView
from app.views.user.user_logout_view import UserLogoutView
from app.views.user.user_profile_view import UserProfileView


from app.views.catalog.catalog_view import CatalogView

from app.views.admin.admin_panel_view import AdminPanelView
from app.views.admin.category.list_category_view import ListCategoryView
from app.views.admin.category.create_category_view import CreateCategoryView
from app.views.admin.category.delete_category_view import DeleteCategoryView


from app.views.admin.product.list_product_view import ListProductView
from app.views.admin.product.create_product_view import CreateProductView
from app.views.admin.product.show_product_view import ShowProductView
from app.views.admin.product.delete_product_view import DeleteProductView
from app.views.admin.product.update_product_view import UpdateProductView
from app.views.user.user_update_view import UpdateUserView

from app.views.product.product_detail_view import ProductDetailView

from app.views.cart.cart_view import CartView
from app.views.cart.add_cart_view import AddCartView
from app.views.cart.remove_cart_view import RemoveCartView
from app.views.cart.delete_cart_view import DeleteCartView

urlpatterns = [
    # Páginas HTML (Template views)
    path('', HomeView.as_view(), name='home'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path("login/", auth_views.LoginView.as_view(template_name="user/login.html", redirect_authenticated_user=True, next_page="/profile" ), name='login'),
    path("logout/", UserLogoutView.as_view(), name='logout'),
    path("register/", UserRegisterView.as_view(), name="register"),

    path('contacto/', ContactView.as_view(), name='contact'),


    path("catalog/", CatalogView.as_view(), name="catalog" ),

    path('user/update/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),
    path('user/delete/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),

    path("catalog/", CatalogView.as_view(), name="catalog" ),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='products/detail'),

    path("admin/", AdminPanelView.as_view(), name="admin"),

    path('admin/categories/',ListCategoryView.as_view(), name='admin/categories'),
    path('admin/categories/create/',CreateCategoryView.as_view(), name='admin/categories/create'),
    path('admin/categories/delete/<int:category_id>',DeleteCategoryView.as_view(), name='admin/categories/delete'),
    path('admin/categories/update/<int:category_id>', UpdateCategoryView.as_view(), name='admin/categories/update'),


    path('admin/products/', ListProductView.as_view(), name='admin/products'),
    path('admin/products/create/', CreateProductView.as_view(), name='admin/products/create'),
    path('admin/products/<int:product_id>/', ShowProductView.as_view(), name='admin/products/show'),
    path('admin/products/delete/<int:product_id>/', DeleteProductView.as_view(), name='admin/products/delete'),
    path('admin/products/update/<int:product_id>/', UpdateProductView.as_view(), name='admin/products/update'),

    # CRUD básico
    path('services/', views.list_services, name='list_services'),
    path('services/create/', views.create_service, name='create_service'),
    path('services/<int:service_id>/', views.get_service, name='get_service'),

    path('orders/create/', views.create_order, name="create_order"),
    path('orders/', views.get_all_orders, name="get_all_orders"),

    path("cart", CartView.as_view(), name="cart"),
    path("cart/add/<int:cart_id>", AddCartView.as_view(), name="cart/add"),
    path("cart/remove/<int:cart_id>", RemoveCartView.as_view(), name="cart/remove"),
    path("cart/delete/<int:cart_id>", DeleteCartView.as_view(), name="cart/delete"),

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
