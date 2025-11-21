from typing import List, Optional
from app.models.cart_item import CartItem
from app.repositories.base_repository import BaseRepository


class CartItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(CartItem)

    def get_user_cart_items(self, user_id: int):
        return self.model.objects.filter(user_id=user_id)

    def get_existing_product_item(self, user_id: int, product_id: int) -> Optional[CartItem]:
        try:
            return self.model.objects.get(user_id=user_id, product_id=product_id)
        except CartItem.DoesNotExist:
            return None

    def get_existing_service_item(self, user_id: int, service_id: int) -> Optional[CartItem]:
        try:
            return self.model.objects.get(user_id=user_id, service_id=service_id)
        except CartItem.DoesNotExist:
            return None
