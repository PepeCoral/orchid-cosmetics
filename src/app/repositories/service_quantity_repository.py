from app.repositories.base_repository import BaseRepository
from app.models import ServiceQuantity


class ServiceQuantityRepository(BaseRepository):
    def __init__(self):
        super().__init__(ServiceQuantity)

    def get_total_quantity_of_a_service(self, service_id, order_id):
        service_quantity = self.model.objects.filter(service_id=service_id, order_id=order_id).first().quantity
        return service_quantity
