from app.repositories.product_repository import ProductRepository
from django.core.exceptions import ValidationError
from app.models import Product

class ProductService():
    def __init__(self):
        self.product_repository = ProductRepository()

    def create_product(self, request, product_data):
        files = request.FILES
        # TODO: añadir repositorio aqui
        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            stock=product_data['stock'],
            fabricator=product_data['fabricator'],
            image_url=files.get('image')
        )
        product.save()

        if 'categories' in product_data:
            product.categories.set(product_data['categories'])

        return product

    def get_product_by_id(self, product_id) -> Product:
        product =  self.product_repository.get_by_id(product_id)

        if product is None:
            raise Product.DoesNotExist(f"No product with id: {product_id}")

        return product

    def get_all_products(self):
        return self.product_repository.get_all()

    def update_product(self, product_id, **data):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValidationError("Producto no encontrado.")

        # 🔹 Lógica adicional
        validation = self.validate_product_data(**data)
        if not validation:
            raise ValidationError("Los datos del producto son inválidos.")

        return self.product_repository.update(product, **data)

    def delete_product(self, product_id):
        return self.product_repository.delete(product_id)

    def get_products_by_category(self, category_id):
        return self.product_repository.get_products_by_category(category_id)
