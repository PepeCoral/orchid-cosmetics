from django.urls import path, include

urlpatterns = [
    path('', include('app.urls.home_urls')),
    path('', include('app.urls.auth_urls')),
    path('', include('app.urls.user_urls')),
    path('', include('app.urls.catalog_urls')),
    path('', include('app.urls.product_urls')),
    path('', include('app.urls.cart_urls')),
    path('', include('app.urls.order_urls')),
    path('', include('app.urls.service_urls')),
    path('', include('app.urls.admin_urls')),
    path('',include('app.urls.stripe_urls'))
]
