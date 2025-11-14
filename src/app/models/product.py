from django.db import models
from .category import Category
from .order import Order

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    fabricator = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="category_products", null=True)

    def __str__(self):
        return self.name

class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="product_id")
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name="product_order_id")
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.identifier}"
