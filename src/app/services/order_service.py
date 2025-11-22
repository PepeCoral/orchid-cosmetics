from app.repositories.order_repository import OrderRepository
from app.models.order import Order

class OrderService():

    def __init__(self):
        self.order_repository = OrderRepository()

    def create_current_order(self,user) -> Order:
        pass
