from app.repositories.base_repository import BaseRepository
from app.models.service import Service

class ServiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Service)

    def get_services_by_category_name(self, category_name:str):
        return self.model.objects.filter(categories__iexact=category_name)
    
    def get_services_by_category_id(self, category_id:str):
        return self.model.objects.filter(categories__id=category_id)
    
    def get_services_by_categories_names(self, category_names:list[str]):
        return self.model.objects.filter(categories__name__in=category_names)
    
    def get_services_between_prices(self, lower_price:float = None, top_price:float = None):
        filters = {}
        
        if lower_price is not None:
            filters["price__gte"] = lower_price
        if top_price is not None:
            filters["price__lte"] = top_price
        
        return Service.objects.filter(**filters)

    def get_services_by_name(self, name:str):
        return Service.objects.filter(name__icontains=name)

    def search(self, filters):
        """
        Busca servicios aplicando múltiples filtros
        """
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
