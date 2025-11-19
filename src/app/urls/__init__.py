from django.urls import include, path

from .home_urls import urlpatterns as home_urls
from .auth_urls import urlpatterns as auth_urls
from .user_urls import urlpatterns as user_urls
from .catalog_urls import urlpatterns as catalog_urls
from .product_urls import urlpatterns as product_urls
from .cart_urls import urlpatterns as cart_urls
from .order_urls import urlpatterns as order_urls
from .service_urls import urlpatterns as service_urls
from .admin_urls import urlpatterns as admin_urls

urlpatterns = (
    home_urls +
    auth_urls +
    user_urls +
    catalog_urls +
    product_urls +
    cart_urls +
    order_urls +
    service_urls +
    admin_urls
)
