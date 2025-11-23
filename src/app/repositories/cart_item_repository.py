from typing import List, Optional
from app.models.cart_item import CartItem
from app.repositories.base_repository import BaseRepository
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

class CartItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(CartItem)

    def get_cart_items(self, owner_filter: dict):
          return self.model.objects.filter(**owner_filter)

    def get_existing_product_item(self, owner_filter: dict, product_id: int) -> Optional[CartItem]:
        filters = owner_filter
        owner_filter.update({"product_id": product_id})

        try:
            return self.model.objects.get(**filters)
        except CartItem.DoesNotExist:
            return None

    def get_existing_service_item(self, owner_filter: dict, service_id: int) -> Optional[CartItem]:
        filters = owner_filter
        filters.update({"service_id": service_id})

        try:
            return self.model.objects.get(**filters)
        except CartItem.DoesNotExist:
            return None

    def get_total_amount(self, owner_filter:dict):
        return self.model.objects.filter(**owner_filter).aggregate(Sum("quantity")).get("quantity__sum")
    def get_by_id_and_owner(self, id: int, owner_filter: dict) -> Optional[CartItem]:
        try:
            filters = owner_filter
            filters.update({"id": id})
            return self.model.objects.get(**filters)
        except ObjectDoesNotExist:
            return None

    def clear_cart(self, owner_filter:dict):
        self.model.objects.filter(**owner_filter).delete()