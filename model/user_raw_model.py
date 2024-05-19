import json
from typing import Optional

from pydantic import (
    BaseModel
)

# All fields are string to allow wrong data
class UserRaw(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    address: Optional[str] = None
    creditCardId: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return json.dumps(self.__dict__)