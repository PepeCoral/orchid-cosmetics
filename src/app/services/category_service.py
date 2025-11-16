from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Q
from app import models
from app.models import Service, Category


class CategoryService():
    
    
    @staticmethod
    def create_category(category_data):
        """
        Crea un nuevo servicio
        """
        category = Category(name=category_data['name'])
        category.save()
        return category
            
    
    @staticmethod
    def get_category_by_id(category_id):
        """
        Obtiene un servicio por su ID
        """
        return Category.objects.get(id=category_id)
    
    @staticmethod
    def get_category_by_name(name):
        return Category.objects.get(name=name)
    
    @staticmethod
    def get_all_categories():
        """
        Obtiene todos los servicios con sus categorías
        """
        return Category.objects.all()
    