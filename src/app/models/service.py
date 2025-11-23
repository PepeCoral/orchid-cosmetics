from django.db import models
from app.models.category import Category
from django.core.validators import MinValueValidator,MaxValueValidator

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0.0),MaxValueValidator(99999999.99)])
    duration_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    department = models.CharField(max_length=100)
    image_url = models.ImageField(null=True)
    isPromoted = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)


    def __str__(self):
        return self.name
