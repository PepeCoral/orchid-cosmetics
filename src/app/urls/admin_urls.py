from django.urls import path
from app.views.admin.admin_panel_view import AdminPanelView

# Category
from app.views.admin.category.list_category_view import ListCategoryView
from app.views.admin.category.create_category_view import CreateCategoryView
from app.views.admin.category.update_category_view import UpdateCategoryView
from app.views.admin.category.delete_category_view import DeleteCategoryView

# Product
from app.views.admin.product.list_product_view import ListProductView
from app.views.admin.product.promote_product_view import PromoteProductView
from app.views.admin.product.demote_product_view import DemoteProductView
from app.views.admin.product.create_product_view import CreateProductView
from app.views.admin.product.show_product_view import ShowProductView
from app.views.admin.product.update_product_view import UpdateProductView
from app.views.admin.product.delete_product_view import DeleteProductView

# Service
from app.views.admin.service.list_service_view import ListServiceView
from app.views.admin.service.promote_service_view import PromoteServiceView
from app.views.admin.service.demote_service_view import DemoteServiceView
from app.views.admin.service.create_service_view import CreateServiceView
from app.views.admin.service.show_service_view import ShowServiceView
from app.views.admin.service.update_service_view import UpdateServiceView
from app.views.admin.service.delete_service_view import DeleteServiceView

# Order
from app.views.admin.order.list_order_view import ListOrderView

urlpatterns = [
    path("admin/", AdminPanelView.as_view(), name="admin"),

    # Categories
    path('admin/categories/', ListCategoryView.as_view(), name='admin/categories'),
    path('admin/categories/create/', CreateCategoryView.as_view(), name='admin/categories/create'),
    path('admin/categories/update/<int:category_id>', UpdateCategoryView.as_view(), name='admin/categories/update'),
    path('admin/categories/delete/<int:category_id>', DeleteCategoryView.as_view(), name='admin/categories/delete'),

    # Products
    path('admin/products/', ListProductView.as_view(), name='admin/products'),
    path('admin/products/promote/<int:product_id>/', PromoteProductView.as_view(),name='admin/products/promote'),
    path('admin/products/demote/<int:product_id>/', DemoteProductView.as_view(),name='admin/products/demote'),
    path('admin/products/create/', CreateProductView.as_view(), name='admin/products/create'),
    path('admin/products/<int:product_id>/', ShowProductView.as_view(), name='admin/products/show'),
    path('admin/products/update/<int:product_id>/', UpdateProductView.as_view(), name='admin/products/update'),
    path('admin/products/delete/<int:product_id>/', DeleteProductView.as_view(), name='admin/products/delete'),

    # Services
    path('admin/cosmeticservices/', ListServiceView.as_view(), name='admin/cosmeticservices'),
    path('admin/cosmeticservices/promote/<int:service_id>/',PromoteServiceView.as_view(), name='admin/cosmeticservices/promote'),
    path('admin/cosmeticservices/demote/<int:service_id>/',DemoteServiceView.as_view(), name='admin/cosmeticservices/demote'),
    path('admin/cosmeticservices/create/', CreateServiceView.as_view(), name='admin/cosmeticservices/create'),
    path('admin/cosmeticservices/<int:service_id>/', ShowServiceView.as_view(), name='admin/cosmeticservices/show'),
    path('admin/cosmeticservices/update/<int:service_id>/', UpdateServiceView.as_view(), name='admin/cosmeticservices/update'),
    path('admin/cosmeticservices/delete/<int:service_id>/', DeleteServiceView.as_view(), name='admin/cosmeticservices/delete'),

    # Orders
    path('admin/orders/', ListOrderView.as_view(), name='admin/orders'),

]
