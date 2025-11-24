from django.db import models
from app.models.product import Product
from app.models.service import Service
import uuid
from app.models.user import User, PaymentMethodOptions


class DeliveryMethodOptions(models.TextChoices):
        CORREO = 'Correo'
        TIENDA = 'Tienda'
        PUNTO_ENTREGA = 'Punto de entrega'

class Order(models.Model):
    def generate_identifier():
         pass
    class StatusOptions(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        SHIPPED = 'shipped', 'Enviado'
        DELIVERED = 'delivered', 'Entregado'



    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="order_user", null=True)
    address = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=StatusOptions.choices, default=StatusOptions.PENDING)
    delivery_method = models.CharField(max_length=20, choices=DeliveryMethodOptions.choices, default=DeliveryMethodOptions.CORREO)
    pay_method = models.CharField(max_length=20, choices=PaymentMethodOptions.choices, default=PaymentMethodOptions.PAYMENT_GATEWAY)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


    def __str__(self):
        return f"Order {self.identifier}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,null=True,blank=True)

    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.item.name} in order {self.order}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    (models.Q(product__isnull=False) & models.Q(service__isnull=True)) |
                    (models.Q(product__isnull=True) & models.Q(service__isnull=False))
                ),
                name="only_one_of_product_or_service_order",
            )
        ]

    @property
    def item(self) -> Product | Service:
        return self.product or self.service
