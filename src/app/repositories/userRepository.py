from app.repositories.baseRepository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    # Ejemplo de métodos personalizados
    def get_by_email(self, email):
        return self.model.objects.filter(email=email).first()

    def get_active_users(self):
        return self.model.objects.filter(is_active=True)
