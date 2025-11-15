from app.repositories.base_repository import BaseRepository
from app.models.product import Product

class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(Product)

    def get_products_by_category(self, category_id):
        return self.model.objects.filter(category_id=category_id)
    
