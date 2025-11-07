from app.repositories.product_repository import ProductRepository
from app.models.category import Category
from app.dtos.create_product_dto import CreateProductDTO

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.user_repository = product_repository

    def deactivate_user(self, user_id):
        return self.user_repository.deactivate(user_id)

    def get_user_details(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if user:
            return {"id": user.id, "username": user.username, "is_active": user.is_active}
        return None

    def create_product(self, product: CreateProductDTO):


        return
