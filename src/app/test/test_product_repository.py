import pytest
from app.models import Product
from app.repositories.product_repository import ProductRepository

@pytest.mark.django_db
class TestProductRepository:
    def setup_method(self):
        self.repo = ProductRepository()

    def test_create_product(self):
        product = self.repo.create(
            name="Lipstick",
            description="A vibrant red lipstick",
            price=19.99,
            stock=100,
            fabricator="BeautyCo",
            image_url="http://example.com/lipstick.jpg"
        )
        assert product.id is not None
        assert product.name == "Lipstick"
        assert product.description == "A vibrant red lipstick"
        assert product.price == 19.99
        assert product.stock == 100
        assert product.fabricator == "BeautyCo"
        assert product.image_url == "http://example.com/lipstick.jpg"
    
    def test_get_by_id(self):
        product = Product.objects.create(
            name="Mascara",
            description="Waterproof mascara",
            price=14.99,
            stock=70,
            fabricator="BeautyCo"
        )
        found = self.repo.get_by_id(product.id)
        assert found == product

    def test_get_all_products(self):
        Product.objects.create(
            name="Eyeliner",
            description="Black eyeliner",
            price=9.99,
            stock=50,
            fabricator="BeautyCo"
        )
        Product.objects.create(
            name="Foundation",
            description="Liquid foundation",
            price=29.99,
            stock=30,
            fabricator="GlamourInc"
        )
        products = self.repo.get_all()
        assert products.count() == 2

    

    def test_update_product(self):
        product = Product.objects.create(
            name="Blush",
            description="Pink blush",
            price=12.99,
            stock=40,
            fabricator="GlamourInc"
        )
        updated = self.repo.update(product.id, price=11.99, stock=45)
        assert updated.price == 11.99
        assert updated.stock == 45
    
    def test_delete_product(self):
        product = Product.objects.create(
            name="Concealer",
            description="Light concealer",
            price=15.99,
            stock=60,
            fabricator="BeautyCo"
        )
        deleted = self.repo.delete(product.id)
        assert deleted is True
        assert Product.objects.count() == 0
    
    def test_get_products_by_category(self):
        from app.models import Category
        category = Category.objects.create(name="Makeup")
        product1 = Product.objects.create(
            name="Highlighter",
            description="Shimmery highlighter",
            price=13.99,
            stock=25,
            fabricator="GlamourInc",
            category=category
        )
        product2 = Product.objects.create(
            name="Bronzer",
            description="Matte bronzer",
            price=14.99,
            stock=30,
            fabricator="BeautyCo",
            category=category
        )
        products = self.repo.get_products_by_category(category.id)
        assert products.count() == 2
        assert product1 in products
        assert product2 in products
    