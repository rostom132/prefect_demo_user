import json

from pydantic import (
    BaseModel,
    EmailStr
)

from model.constants import Gender

class BaseUserModel(BaseModel):
    name: str
    age: int
    gender: Gender
    email: EmailStr
    phoneNumber: str
    address: str
    creditCardId: str
    weight: float
    height: float

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return json.dumps(self.__dict__)
