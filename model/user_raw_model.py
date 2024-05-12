import json

# All fields are string to allow wrong data
class UserRaw:
    name: str
    age: str
    gender: str
    email: str
    phoneNumber: str
    address: str
    creditCardId: str

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return json.dumps(self.__dict__)