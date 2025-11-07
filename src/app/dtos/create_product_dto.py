# myapp/dtos/product_dto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateProductDTO:
    name: str
    description: str
    price: float
    stock: int
    fabricator: str
    image_url: Optional[str] = ""
    category_id: Optional[int] = None
