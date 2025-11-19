from django.urls import path
from app.views.catalog.catalog_view import CatalogView

urlpatterns = [
    path("catalog/", CatalogView.as_view(), name="catalog"),
]
