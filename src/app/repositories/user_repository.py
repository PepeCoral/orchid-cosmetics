from app.repositories.base_repository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    # Ejemplo de métodos personalizados

    def is_admin(self, role):
        return role == User.RoleOptions.ADMIN
    
    def get_address(self):
        return self.model.objects.values_list('address', flat=True).first()
    

    

