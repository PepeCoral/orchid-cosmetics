from app.repositories.product_repository import ProductRepository
from app.models.category import Category
from app.models.product import Product
from app.dtos.create_product_dto import CreateProductDTO

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository: ProductRepository = product_repository

    def create_product(self, product: CreateProductDTO):
        product_to_create: Product = Product()

        product_to_create.name = product.name

        return self.product_repository.create(product_to_create)
