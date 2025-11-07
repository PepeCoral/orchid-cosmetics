from django.db import models
from .user import User

class Order(models.Model):

    class StatusOptions(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELED = 'canceled', 'Canceled'

        
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name="order_user")
    address = models.CharField(max_length=200)
    payMethod = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=StatusOptions.choices, default=StatusOptions.PENDING)
    delivery_method = models.CharField(max_length=50)
    identifier = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Order {self.identifier} by {self.user.username}"