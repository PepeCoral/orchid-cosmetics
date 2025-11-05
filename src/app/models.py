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


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    fabricator = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 related_name="products", null=True)


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField()
    department = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 related_name="services", null=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name="order_user")
    address = models.CharField(max_length=200)
    payMethod = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    delivery_method = models.CharField(max_length=50)
    identifier = models.CharField(max_length=100)


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                related_name="product")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name="order")
    quantity = models.IntegerField()


class ServiceQuantity(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, 
                                related_name="service")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                              related_name="order")
    quantity = models.IntegerField()