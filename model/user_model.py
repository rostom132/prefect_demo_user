import json

from utils.repairer import auto_correct
from pydantic import (
    BaseModel,
    model_validator
)

class UserModel(BaseModel):
    name: str
    age: int
    gender: str
    email: str
    phoneNumber: str
    address: str
    creditCardId: str
    weight: float
    height: float

    @model_validator(mode='before')
    @classmethod
    def check_user_data(cls, data):
        if isinstance(data, dict):
            if not data['gender']:
                data['gender'] = auto_correct('gender', data['gender'], data)
        return data

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return json.dumps(self.__dict__)
