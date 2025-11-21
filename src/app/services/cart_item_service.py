from typing import List, Optional
from django.core.exceptions import ValidationError, PermissionDenied
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.service import Service
from app.repositories.cart_item_repository import CartItemRepository
from django.http import HttpRequest
from django.contrib.auth.models import AbstractUser, AnonymousUser


class CartService:
    def __init__(self):
        self.cart_repo = CartItemRepository()

    def _create_owner_filter(self, request: HttpRequest):
        user: AbstractUser | AnonymousUser = request.user

        if user.is_anonymous:
            if not request.session.session_key:
              request.session.create()
            return {"session_key": request.session.session_key}
        else:
            return {"user_id": user.id}


    def add_item(self, request:HttpRequest, item: Product | Service, quantity: int = 1) -> List[CartItem]:

        owner_filter = self._create_owner_filter(request)


        if isinstance(item, Product):
            cart_item = self.cart_repo.get_existing_product_item(owner_filter, item.id)
            if cart_item:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                if request.user.is_anonymous:
                  self.cart_repo.create(
                      session_key=request.session.session_key,
                      product=item,
                      quantity=quantity,
                  )
                else:
                    self.cart_repo.create(
                      user=request.user,
                      product=item,
                      quantity=quantity,
                  )

        else:
            cart_item = self.cart_repo.get_existing_service_item(owner_filter, item.id)
            if cart_item:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                if request.user.is_anonymous:
                  self.cart_repo.create(
                      session_key=request.session.session_key,
                      service=item,
                      quantity=quantity,
                  )
                else:
                    self.cart_repo.create(
                      user=request.user,
                      service=item,
                      quantity=quantity,
                  )

        return list(self.cart_repo.get_cart_items(owner_filter))

    def get_cart_items(self, request) -> List[CartItem]:
        owner_filter = self._create_owner_filter(request)
        return list(self.cart_repo.get_cart_items(owner_filter))

    def get_total(self, request) -> float:
        return sum(item.subtotal() for item in self.get_cart_items(request))

    def add_one_by_id(self, cart_item_id: int, request) -> CartItem:
        owner_filter = self._create_owner_filter(request)
        cart_item = self.cart_repo.get_by_id_and_owner(cart_item_id, owner_filter)
        if not cart_item:
            raise ValidationError("Cart item not found.")

        cart_item.quantity += 1
        cart_item.save()
        return cart_item

    def remove_one_by_id(self, cart_item_id: int, request) -> Optional[CartItem]:
        owner_filter = self._create_owner_filter(request)
        cart_item = self.cart_repo.get_by_id_and_owner(cart_item_id, owner_filter)
        if not cart_item:
            raise ValidationError("Cart item not found.")
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return cart_item

        cart_item.delete()
        return None

    def delete_item_by_id(self, cart_item_id: int, request) -> bool:
        owner_filter = self._create_owner_filter(request)
        cart_item = self.cart_repo.get_by_id_and_owner(cart_item_id, owner_filter)
        if not cart_item:
            raise ValidationError("Cart item not found.")
        cart_item.delete()
        return True
