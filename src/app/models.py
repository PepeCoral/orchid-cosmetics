from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, default='')
    payMethod = models.CharField(max_length=50, blank=True, default='')
    role = models.CharField(max_length=20, blank=True, default='')
    
    def __str__(self):
        return f"{self.name} {self.surname} - {self.email}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                related_name="product_id")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name="product_order_id")
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.identifier}"


class ServiceQuantity(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, 
                                related_name="service_id")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name="service_order_id")
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.service.name} in order {self.order.identifier}"