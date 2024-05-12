from faker import Faker
from model.user_raw_model import UserRaw
faker = Faker()

GENDERS = ['male', 'female']; 

def getWrongName():
    return ''

def getWrongAge():
    return faker.random_int(min= -100, max= -1)

def getWrongGender():
    return 'UNEXPECTED_GENDER'

def getWrongPhoneNumber():
    return '123a123a'

def getWrongCreaditCard():
    return 'WRONGWRONG'

wrongFuncMap = {
    'name': getWrongName,
    'age': getWrongAge,
    'gender': getWrongGender,
    'phoneNumber': getWrongPhoneNumber,
    'creditCardId': getWrongCreaditCard
}

def getRightUserData():
    userData = UserRaw()
    userData.name = faker.name()
    userData.age = faker.random_int(min= 5, max= 100)
    userData.gender = faker.random_element(GENDERS)
    userData.email = faker.email()
    userData.phoneNumber = faker.phone_number()
    userData.address = faker.address()
    userData.creditCardId = faker.credit_card_number()

    return userData

def getWrongUserData():
    userData = UserRaw()
    userData.name = faker.name()
    userData.age = faker.random_int(min= 5, max= 100)
    userData.gender = faker.random_element(GENDERS)
    userData.email = faker.email()
    userData.phoneNumber = faker.phone_number()
    userData.address = faker.address()
    userData.creditCardId = faker.credit_card_number()

    # Overwrite some wrong data
    randomObjects = faker.random_choices(list(wrongFuncMap.items()))
    for property, getterWrongData in randomObjects:
        setattr(userData, property, getterWrongData())
    
    return userData

def getRandomUserData():
    if (faker.random_number(min=0, max=100) < 30):
        return getWrongUserData()
    return getRightUserData()

if __name__ == "__main__":
    for i in range(10):
        print(getRightUserData())

    for i in range(3):
        print(getWrongUserData())