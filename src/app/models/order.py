import secrets
from django.db import models
from .user import User

class Order(models.Model):
    def generate_identifier():
        return ''.join(secrets.choice('0123456789') for _ in range(6))

    class StatusOptions(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELED = 'canceled', 'Canceled'
    
    class DeliveryMethods(models.TextChoices):
        PUNTO_DE_RECOGIDA = 'En punto de recogida'
        ADDRESS = 'En una dirección para la entrega'
        SHOP = 'Recoger en la tienda más cercana'

        
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name="order_user", null=True)
    address = models.CharField(max_length=200)
    payMethod = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=StatusOptions.choices, default=StatusOptions.PENDING)
    delivery_method = models.CharField(max_length=50, choices=DeliveryMethods.choices)
    identifier = models.CharField(max_length=6, unique=True, default=generate_identifier)
    products = models.ManyToManyField("Product", through="ProductQuantity")
    services = models.ManyToManyField("Service", through="ServiceQuantity")


    def __str__(self):
        return f"Order {self.identifier} by {self.user.username}"
    
    