from django.urls import path
from app.views.product.product_detail_view import ProductDetailView

urlpatterns = [
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='products/detail'),
]
