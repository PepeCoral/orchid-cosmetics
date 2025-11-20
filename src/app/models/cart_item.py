# app/models/cart_item.py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from app.models.user import User


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")

    # Generic relation to Product or Service
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")

    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def subtotal(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"
    
    def stripify(self):
        return {
            "price_data": {
                "currency": "eur", 
                "product_data": {
                    "name": self.item.name,
                    "description":self.item.description
                },
                "unit_amount": int(self.item.price * 100)
            },
            "quantity": self.quantity
        }
