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
        product_to_create.description = product.description
        product_to_create.price = product.price
        product_to_create.stock = product.stock
        product_to_create.fabricator = product.fabricator
        product_to_create.image_url = product.image_url
        # TODO: Link to a Category


        return self.product_repository.create(name=product.name, description=product.description, price=product.price,
                                               stock=product.stock, fabricator=product.fabricator, image_url=product.image_url)

    def get_by_id(self, id: int) -> Product:
        return self.product_repository.get_by_id(id)

    def get_all(self) -> list[Product]:
        return self.product_repository.get_all()
