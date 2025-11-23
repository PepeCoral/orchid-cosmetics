from app.repositories.base_repository import BaseRepository
from app.models.order import Order
from app.repositories.product_repository import ProductRepository

class OrderRepository(BaseRepository):
    def __init__(self):
        super().__init__(Order)
        self.product_repository = ProductRepository()

    def get_by_user_id(self, user_id):
        return self.model.objects.filter(user_id=user_id)

    def get_orders_by_user(self, user_id):
        return self.model.objects.filter(user_id=user_id)
    
    def get_orders_by_status(self, status):
        return self.model.objects.filter(status=status)
    
    def get_order_by_identifier(self, identifier):
        return self.model.objects.filter(identifier=identifier)
    
    def get_number_of_products(self, product_id, order_id):
        product = self.product_repository.get_by_id(product_id)
        order = self.get_by_id(order_id)
        
