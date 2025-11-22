from django.db import models
from django.contrib.auth.models import AbstractUser

class RoleOptions(models.TextChoices):
        USER = 'User'
        ADMIN = 'Admin'

class PaymentMethodOptions(models.TextChoices):
    CASH_ON_DELIVERY = 'contrarembolso', 'Contrarembolso'
    PAYMENT_GATEWAY = 'pasarela', 'Pasarela de Pago'

class User(AbstractUser):


    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True,default=None)
    pay_method = models.CharField(max_length=50, null=True,default=None)
    role = models.CharField(max_length=20, choices=RoleOptions.choices, default=RoleOptions.USER)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email} - {self.username}"

    def is_admin(self):
        return self.role == RoleOptions.ADMIN
