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

