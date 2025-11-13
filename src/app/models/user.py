from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    class RoleOptions(models.TextChoices):
        USER = 'User'
        ADMIN = 'Admin'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True, default='')
    pay_method = models.CharField(max_length=50, blank=True, default='')
    role = models.CharField(max_length=20, choices=RoleOptions.choices, default=RoleOptions.USER)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    def is_admin(self):
        return self.role == RoleOptions.ADMIN
