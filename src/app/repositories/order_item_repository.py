from typing import List, Optional
from app.models.order import OrderItem
from app.repositories.base_repository import BaseRepository
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F, Case, When, DecimalField


class OrderItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(OrderItem)

    def get_total_amount(self, order_id:int) -> float:

        total = OrderItem.objects.filter(order__id=order_id).annotate(
            item_price=Case(
                When(product__isnull=False, then=F('product__price')),
                When(service__isnull=False, then=F('service__price')),
                output_field=DecimalField()
            )
        ).aggregate(
            total_cost=Sum(F('item_price') * F('quantity'))
        )['total_cost']

        return total
    
    def get_items_by_order_id(self, order_id:int) -> List[OrderItem]:
        return self.model.objects.filter(order__id=order_id)