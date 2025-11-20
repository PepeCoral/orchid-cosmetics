from app.repositories.product_repository import ProductRepository
from django.core.exceptions import ValidationError
from app.models import Product

class ProductService():
    def __init__(self):
        self.product_repository = ProductRepository()

    def create_product(self, request, product_data):

        if(product_data["price"] < 0):
            raise ValidationError("Price cannot be negative")
        if(product_data["stock"] < 0):
            raise ValidationError("Stock cannot be negative")

        files = request.FILES
        product_data["image_url"] = files.get("image_url")
        categories = product_data.pop("categories")
        product = self.product_repository.create(**product_data)
        product.categories.set(categories)
        return product

    def get_product_by_id(self, product_id) -> Product:
        product =  self.product_repository.get_by_id(product_id)

        if product is None:
            raise Product.DoesNotExist(f"No product with id: {product_id}")

        return product

    def get_all_products(self):
        return self.product_repository.get_all()

    def get_top_products(self):
        return self.product_repository.get_all_top_products()

    def update_top_product(self,product_id,request):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValidationError("Producto no encontrado.")
        top = request.POST["top"]
        updated_product = self.product_repository.update(product_id,top=top)
        return updated_product

    def update_product(self, product_id, product_data, request):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValidationError("Producto no encontrado.")

        categories = product_data.pop("categories")
        files = request.FILES
        product_data["image_url"] = files.get("image_url")
        updated_product =  self.product_repository.update(product_id, **product_data)

        updated_product.categories.set(categories)
        return updated_product


    def delete_product(self, product_id):
        return self.product_repository.delete(product_id)

    def get_products_by_category(self, category_id):
        return self.product_repository.get_products_by_category(category_id)

    def search_products(self, filters: dict):
        return self.product_repository.search(filters)
