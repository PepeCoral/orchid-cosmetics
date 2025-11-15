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
    
    def get_services_between_prices(self, lower_price:float = None,top_price:float = None):
        filters = {}
        
        if lower_price is not None:
            filters["price__gte"] = lower_price
        if top_price is not None:
            filters["price__lte"] = top_price
        
        return Service.objects.filter(**filters)

    def get_services_by_name(self, name:str):
        return Service.objects.filter(name__icontains=name)
