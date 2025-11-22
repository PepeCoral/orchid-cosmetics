from typing import List, Optional
from app.models.order import OrderItem
from app.repositories.base_repository import BaseRepository
from django.core.exceptions import ObjectDoesNotExist

class OrderItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(OrderItem)