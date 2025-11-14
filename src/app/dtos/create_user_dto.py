from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateUserDTO:
    username: str
    fist_name: str
    last_name: str
    email: str
    address: str
    pay_method: str
