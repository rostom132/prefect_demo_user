import json

from pydantic import (
    BaseModel
)

class UserModel(BaseModel):
    name: str
    age: int
    gender: str
    email: str
    phoneNumber: str
    address: str
    creditCardId: str

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return json.dumps(self.__dict__)
