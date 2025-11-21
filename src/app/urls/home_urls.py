from django.urls import path
from app.views.home.home_view import HomeView
from app.views.static_pages import ContactView
from app.views.home.search_product_view import SearchProductView
from app.views.home.search_service_view import SearchServiceView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacto/', ContactView.as_view(), name='contact'),
    path('search/product', SearchProductView.as_view(), name='search/product'),
    path('search/service',SearchServiceView.as_view(), name='search/service')
]
