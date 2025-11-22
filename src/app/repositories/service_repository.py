from app.repositories.base_repository import BaseRepository
from app.models.service import Service

class ServiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Service)

    def get_services_by_category_id(self, category_id:str):
        return Service.objects.filter(categories__id=category_id)

    def search(self, filters):
        qs = Service.objects.all()

        name = filters.get('name')
        min_price = filters.get('min_price')
        max_price = filters.get('max_price')
        department = filters.get('department')
        categories = filters.get('categories')

        if name:
            qs = qs.filter(name__icontains=name)

        if min_price is not None:
            qs = qs.filter(price__gte=min_price)

        if max_price is not None:
            qs = qs.filter(price__lte=max_price)

        if department:
            qs = qs.filter(department__icontains=department)

        if categories:
            qs = qs.filter(categories__in=categories).distinct()

        return qs

    def get_all_promoted_services(self):
        qs = Service.objects.filter(isPromoted=True)
        return qs