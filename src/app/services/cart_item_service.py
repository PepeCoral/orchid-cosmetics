from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError, PermissionDenied
from app.models.cart_item import CartItem
from app.repositories.cart_item_repository import CartItemRepository


class CartService:
    def __init__(self):
        self.cart_repo = CartItemRepository()

    def add_item(self, user, item, quantity=1):
        content_type = ContentType.objects.get_for_model(item)
        cart_item = self.cart_repo.get_user_cart_item(user.id, content_type, item.id)

        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            self.cart_repo.create(
                user=user,
                content_type=content_type,
                object_id=item.id,
                quantity=quantity
            )
        return self.cart_repo.get_user_cart_items(user.id)

    def remove_item(self, user, item):
        content_type = ContentType.objects.get_for_model(item)
        cart_item = self.cart_repo.get_user_cart_item(user.id, content_type, item.id)
        if cart_item:
            cart_item.delete()
        return self.cart_repo.get_user_cart_items(user.id)

    def clear_cart(self, user):
        return self.cart_repo.get_user_cart_items(user.id).delete()

    def get_cart_items(self, user):
        return self.cart_repo.get_user_cart_items(user.id)

    def get_total(self, user):
        return sum(item.subtotal() for item in self.get_cart_items(user))

    def add_one_by_id(self, cart_item_id, user):
      cart_item = self.cart_repo.get_by_id(cart_item_id)
      if not cart_item:
          raise ValidationError("Cart item not found.")
      if cart_item.user != user:
          raise PermissionDenied("Cannot modify another user's cart item.")
      cart_item.quantity += 1
      cart_item.save()
      return cart_item

    def remove_one_by_id(self, cart_item_id, user):
        cart_item = self.cart_repo.get_by_id(cart_item_id)
        if not cart_item:
            raise ValidationError("Cart item not found.")
        if cart_item.user != user:
            raise PermissionDenied("Cannot modify another user's cart item.")
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return cart_item
        else:
            # If quantity is 1, delete the item
            cart_item.delete()
            return None

    def delete_item_by_id(self, cart_item_id, user):
        cart_item = self.cart_repo.get_by_id(cart_item_id)
        if not cart_item:
            raise ValidationError("Cart item not found.")
        if cart_item.user != user:
            raise PermissionDenied("Cannot delete another user's cart item.")
        cart_item.delete()
        return True
