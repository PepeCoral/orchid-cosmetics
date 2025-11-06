from django.contrib import admin
from .models import User, Category, Product, Service, Order, ProductQuantity, ServiceQuantity
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(ProductQuantity)
admin.site.register(ServiceQuantity)
