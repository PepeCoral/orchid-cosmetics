from app.models.cart_item import CartItem
from app.repositories.base_repository import BaseRepository


class CartItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(CartItem)

    def get_user_cart_items(self, user_id: int):
        return self.model.objects.filter(user_id=user_id)

    def get_user_cart_item(self, user_id: int, content_type, object_id):
        try:
            return self.model.objects.get(user_id=user_id, content_type=content_type, object_id=object_id)
        except self.model.DoesNotExist:
            return None
