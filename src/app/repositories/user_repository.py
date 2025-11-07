from app.repositories.base_repository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        return self.model.objects.filter(email=email)

    def get_address(self):
        return self.model.objects.values_list('address', flat=True).distinct()
    

    

