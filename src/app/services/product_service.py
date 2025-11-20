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

    def get_promoted_products(self):
        return self.product_repository.get_all_promoted_products()

    def promote_product(self,product_id):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValidationError("Producto no encontrado.")
        updated_product = self.product_repository.update(id=product_id, isPromoted=True)
        return updated_product
    
    def demote_product(self,product_id):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValidationError("Producto no encontrado.")
        updated_product = self.product_repository.update(id=product_id, isPromoted=False)
        return updated_product

    def update_product(self, product_id, product_data, request):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValidationError("Producto no encontrado.")

        # Validaciones
        if "price" in product_data and product_data["price"] < 0:
            raise ValidationError("El precio no puede ser negativo")
        if "stock" in product_data and product_data["stock"] < 0:
            raise ValidationError("El stock no puede ser negativo")

        # Manejar imagen si se envió
        files = request.FILES
        if 'image_url' in files:
            product_data["image_url"] = files.get("image_url")

        # Manejar categorías si se enviaron
        categories = None
        if "categories" in product_data:
            categories = product_data.pop("categories")

        # Actualizar servicio
        updated_product = self.product_repository.update(product_id, **product_data)

        # Actualizar categorías si se proporcionaron
        if categories is not None:
            updated_product.categories.set(categories)

        return updated_product


    def delete_product(self, product_id):
        return self.product_repository.delete(product_id)

    def get_products_by_category(self, category_id):
        return self.product_repository.get_products_by_category(category_id)

    def search_products(self, filters: dict):
        return self.product_repository.search(filters)
