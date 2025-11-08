from app.repositories.base_repository import BaseRepository
from app.models import ProductQuantity
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository

class ProductQuantityRepository(BaseRepository):
    def __init__(self):
        super().__init__(ProductQuantity)
        self.prod_repo = ProductRepository()
        self.order_repo = OrderRepository()

    def get_total_quantity_of_a_product(self, product_id, order_id):
        prod_quantity = self.model.objects.filter(product_id=product_id, order_id=order_id).first().quantity
        return prod_quantity
