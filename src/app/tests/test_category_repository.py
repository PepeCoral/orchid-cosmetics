from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from django.test import TestCase
from django.db import IntegrityError

class TestCategoryRepository(TestCase):
    def setUp(self):
        super().setUp()
        self.category_repo = CategoryRepository()

    def create_category(self, name="Electronics"):
        return self.category_repo.create(name=name)
    
    def test_create_category(self):
        category = self.create_category()
        self.assertIsNotNone(category.id)
        self.assertEqual(category.name, "Electronics")

    def test_get_all_categories(self):
        Category.objects.create(name="Books")
        Category.objects.create(name="Clothing")

        categories = self.category_repo.get_all()
        self.assertEqual(categories.count(), 3)

    def test_get_by_id(self):
        category = Category.objects.create(name="Toys")

        found = self.category_repo.get_by_id(category.id)
        self.assertEqual(found, category)

    def test_update_category(self):
        category = Category.objects.create(name="Home Appliances")

        updated = self.category_repo.update(category.id, name="Kitchen Appliances")
        self.assertEqual(updated.name, "Kitchen Appliances")

    def test_delete_category(self):
        category = Category.objects.create(name="Sports")
        deleted = self.category_repo.delete(category.id)
        self.assertTrue(deleted)
        self.assertEqual(Category.objects.count(), 1)
