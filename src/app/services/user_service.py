from app.repositories.user_repository import UserRepository
from app.models.user import User

class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def create(self, user: User):
        
        return self.user_repo.create(user)
        