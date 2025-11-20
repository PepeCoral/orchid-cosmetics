from django.urls import path
from app.views.catalog.product_catalog_view import ProductCatalogView
from app.views.catalog.service_catalog_view import ServiceCatalogView

urlpatterns = [
    path("catalog/products/", ProductCatalogView.as_view(), name="product_catalog"),
    path("catalog/services/", ServiceCatalogView.as_view(), name="service_catalog"),
]
