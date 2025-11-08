from app.repositories.base_repository import BaseRepository
from app.models.order import Order

class OrderRepository(BaseRepository):
    def __init__(self):
        super().__init__(Order)

    def get_orders_by_user(self, user_id):
        return self.model.objects.filter(user_id=user_id)

    def get_order_by_id(self, order_id):
        return self.model.objects.filter(id=order_id).first()
    
    def get_orders_by_status(self, status):
        return self.model.objects.filter(status=status)
    
    def get_orders_by_identifier(self, identifier):
        return self.model.objects.filter(identifier=identifier)