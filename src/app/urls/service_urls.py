from django.urls import path
from app.views.service.reserve_now_view import ReserveNowView
from app.views.service.service_detail_view import ServiceDetailView

urlpatterns = [
    path('services/<int:service_id>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/reserve-now/<int:service_id>/', ReserveNowView.as_view(), name='service_reserve_now'),

]
