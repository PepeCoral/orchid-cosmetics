from typing import List, Optional
from django.core.exceptions import ValidationError, PermissionDenied
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.service import Service
from app.repositories.cart_item_repository import CartItemRepository


class CartService:
    def __init__(self):
        self.cart_repo = CartItemRepository()

    def add_item(self, user, item: Product | Service, quantity: int = 1) -> List[CartItem]:
        if isinstance(item, Product):
            cart_item = self.cart_repo.get_existing_product_item(user.id, item.id)
            if cart_item:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                self.cart_repo.create(
                    user=user,
                    product=item,
                    quantity=quantity,
                )
        else:
            cart_item = self.cart_repo.get_existing_service_item(user.id, item.id)
            if cart_item:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                self.cart_repo.create(
                    user=user,
                    service=item,
                    quantity=quantity,
                )

        return list(self.cart_repo.get_user_cart_items(user.id))

    def remove_item(self, user, item: Product | Service) -> List[CartItem]:
        if isinstance(item, Product):
            cart_item = self.cart_repo.get_existing_product_item(user.id, item.id)
        else:
            cart_item = self.cart_repo.get_existing_service_item(user.id, item.id)

        if cart_item:
            cart_item.delete()

        return list(self.cart_repo.get_user_cart_items(user.id))

    def clear_cart(self, user):
        return self.cart_repo.get_user_cart_items(user.id).delete()

    def get_cart_items(self, user) -> List[CartItem]:
        return list(self.cart_repo.get_user_cart_items(user.id))

    def get_total(self, user) -> float:
        return sum(item.subtotal() for item in self.get_cart_items(user))

    def add_one_by_id(self, cart_item_id: int, user) -> CartItem:
        cart_item = self.cart_repo.get_by_id(cart_item_id)
        if not cart_item:
            raise ValidationError("Cart item not found.")
        if cart_item.user != user:
            raise PermissionDenied("Cannot modify another user's cart item.")

        cart_item.quantity += 1
        cart_item.save()
        return cart_item

    def remove_one_by_id(self, cart_item_id: int, user) -> Optional[CartItem]:
        cart_item = self.cart_repo.get_by_id(cart_item_id)
        if not cart_item:
            raise ValidationError("Cart item not found.")
        if cart_item.user != user:
            raise PermissionDenied("Cannot modify another user's cart item.")

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return cart_item

        cart_item.delete()
        return None

    def delete_item_by_id(self, cart_item_id: int, user) -> bool:
        cart_item = self.cart_repo.get_by_id(cart_item_id)
        if not cart_item:
            raise ValidationError("Cart item not found.")
        if cart_item.user != user:
            raise PermissionDenied("Cannot delete another user's cart item.")

        cart_item.delete()
        return True
