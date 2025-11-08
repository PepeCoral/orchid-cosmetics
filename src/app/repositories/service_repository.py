from app.repositories.base_repository import BaseRepository
from app.models.service import Service

class ServiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Service)

    # Ejemplo de métodos personalizados

    def get_services_by_category(self, category_name):
        return self.model.objects.filter(category=category_name)