from django.db import models
from app.models.category import Category
from app.models.order import Order
from django.core.validators import MinValueValidator,MaxValueValidator

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0.0),MaxValueValidator(99999999.99)])
    stock = models.IntegerField(validators=[MinValueValidator(0, "No puede haber stock negativo")])
    fabricator = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='products/',null=True)
    categories = models.ManyToManyField(Category)



    def __str__(self):
        return self.name

class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order}"
    
    def set_product(self, product):
        self.product_id.set(product.id)
    
    def set_order(self, order):
        self.order.set(order)
