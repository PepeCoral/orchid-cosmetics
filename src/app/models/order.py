from django.db import models
from .user import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name="order_user")
    address = models.CharField(max_length=200)
    payMethod = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    delivery_method = models.CharField(max_length=50)
    identifier = models.CharField(max_length=100)

    def __str__(self):
        return f"Order {self.identifier} by {self.user.name}"