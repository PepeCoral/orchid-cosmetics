from django.contrib import admin
from .models import User, Category, Product, Service, Order, CartItem, OrderItem
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(OrderItem)
