from app.models import Category
from app.repositories import category_repository
from app.repositories.category_repository import CategoryRepository
from django.core.exceptions import ValidationError


class CategoryService():
    def __init__(self):
        self.category_repository = CategoryRepository()

    def create_category(self,category_data):
        return self.category_repository.create(**category_data)

    def list_categories(self):
        return self.category_repository.get_all()

    def delete_category(self, category_id):
        return self.category_repository.delete(category_id)

    def update_category(self, category_id, category_data):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise ValidationError("Categoría no encontrada.")

        updated_category = self.category_repository.update(category_id, **category_data)
        return updated_category


    def get_category_by_id(self, category_id):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise ValidationError(f"Categoría con ID {category_id} no encontrada.")
        return category
