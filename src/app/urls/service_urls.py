from django.urls import path
from app.views.service.service_detail_view import ServiceDetailView

urlpatterns = [
    path('services/<int:service_id>/', ServiceDetailView.as_view(), name='service_detail'),
]
