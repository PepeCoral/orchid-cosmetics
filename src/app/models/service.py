from django.db import models 
from .category import Category
from .order import Order
from django.core.validators import MinValueValidator

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    duration_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    department = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='services/', null=True)
    categories = models.ManyToManyField(Category)


    def __str__(self):
        return self.name
    

class ServiceQuantity(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.service.name} in order {self.order.identifier}"