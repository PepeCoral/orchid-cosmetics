from django.urls import path
from app.views.product.buy_now_view import BuyNowView
from app.views.product.product_detail_view import ProductDetailView

urlpatterns = [
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='products/detail'),
    path('products/buy-now/<int:product_id>', BuyNowView.as_view(), name='products/buy-now'),
]
