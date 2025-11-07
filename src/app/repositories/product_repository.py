from app.repositories.base_repository import BaseRepository
from app.models.product import Product

class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(Product)
