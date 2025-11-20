from django.urls import path
from app.views.home_view import HomeView
from app.views.static_pages import ContactView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacto/', ContactView.as_view(), name='contact'),
]
