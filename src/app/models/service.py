from django.db import models 
from .category import Category
from .order import Order

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField()
    department = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 related_name="category_services", null=True)

    def __str__(self):
        return self.name
    

class ServiceQuantity(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, 
                                related_name="service_id")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name="service_order_id")
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.service.name} in order {self.order.identifier}"