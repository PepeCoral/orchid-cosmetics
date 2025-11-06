from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, default='')
    payMethod = models.CharField(max_length=50, blank=True, default='')
    role = models.CharField(max_length=20, blank=True, default='')
    
    def __str__(self):
        return f"{self.name} {self.surname} - {self.email}"