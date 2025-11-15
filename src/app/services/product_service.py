from app.repositories.product_repository import ProductRepository
from django.core.exceptions import ValidationError

class ProductService():
    def __init__(self):
        self.repository = ProductRepository()

    def validate_product_data(self, **data):
        # 🔹 Validaciones básicas
        if "name" not in data or not data["name"]:
            raise ValidationError("El nombre del producto es obligatorio.")
        
        if "description" not in data or not data["description"]:
            raise ValidationError("La descripción del producto es obligatoria.")
        
        if "price" not in data or data["price"] <= 0:
            raise ValidationError("El precio debe ser mayor que 0.")

        if "stock" not in data or data["stock"] < 0:
            raise ValidationError("El stock no puede ser negativo.")
        
        if "fabricator" not in data or not data["fabricator"]:
            raise ValidationError("El fabricante del producto es obligatorio.")
        
        if "image_url" in data and data["image_url"]:
            # Aquí podrías agregar una validación más robusta para URLs
            if not data["image_url"].startswith("http"):
                raise ValidationError("La URL de la imagen no es válida.")
        
        if "category" in data and data["category"] is not None:
            raise ValidationError("La categoría especificada no existe.")

        return True

    def create_product(self, name, description, price, stock, fabricator, image_url=None, category=None):
        # 🔹 Regla de negocio: no se permiten nombres duplicados
        validation = self.validate_product_data(
            name=name, description=description, price=price, 
            stock=stock, fabricator=fabricator, image_url=image_url, 
            category=category)

        if not validation:
            raise ValidationError("Los datos del producto son inválidos.")

        # 🔹 Crear producto
        return self.repository.create(
            name=name, description=description, price=price, 
            stock=stock, fabricator=fabricator, image_url=image_url, 
            category=category)

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
        
