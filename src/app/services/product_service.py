from app.repositories.product_repository import ProductRepository
from django.core.exceptions import ValidationError

class ProductService():
    def __init__(self):
        self.repository = ProductRepository()

    def create_product(self, request, product_data):
        # 🔹 Regla de negocio: no se permiten nombres duplicados
        files = request.FILES

        product = self.repository.create(product_data)
        product.save()

        if 'categories' in product_data:
            product.categories.set(product_data['categories'])

        return product
        # 🔹 Crear producto

    def get_product_by_id(self, product_id):
        return self.repository.get_by_id(product_id)
    
    def get_all_products(self):
        return self.repository.get_all()

    def update_product(self, product_id, **data):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValidationError("Producto no encontrado.")

        # 🔹 Lógica adicional
        validation = self.validate_product_data(**data)
        if not validation:
            raise ValidationError("Los datos del producto son inválidos.")

        return self.repository.update(product, **data)

    def delete_product(self, product_id):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValidationError("Producto no encontrado.")

        return self.repository.delete(product)
    
    def get_products_by_category(self, category_id):
        return self.repository.get_products_by_category(category_id)
        
