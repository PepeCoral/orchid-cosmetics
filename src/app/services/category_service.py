from app.models import Category
from app.repositories.category_repository import CategoryRepository


class CategoryService():
    def __init__(self):
        self.category_repository = CategoryRepository()

    def create_category(self,category_data):
        return self.category_repository.create(**category_data)

    def list_categories(self):
        return self.category_repository.get_all()

    def delete_category(self, category_id):
        return self.category_repository.delete(category_id)
