from django.db import models
from django.core.validators import MinValueValidator
from app.models.user import User
from app.models.product import Product
from app.models.service import Service


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")

    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    (models.Q(product__isnull=False) & models.Q(service__isnull=True)) |
                    (models.Q(product__isnull=True) & models.Q(service__isnull=False))
                ),
                name="only_one_of_product_or_service",
            )
        ]

    @property
    def item(self) -> Product | Service:
        return self.product or self.service

    def subtotal(self) -> float:
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"
