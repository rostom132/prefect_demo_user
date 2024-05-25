from faker import Faker
from model.user_raw_model import UserRaw
faker = Faker()

GENDERS = ['male', 'female', 'm', 'f', 'strong', 'weak']

WRONG_GENDERS = ['jkahfd', 'jkgfgk', 'asdfasd']
WRONG_EMAILS = ['suidfhsuidf83@asd', 'rbdkjfgdf@13213']

def getWrongAge():
    return faker.random_int(min= -100, max= -1)

def getWrongGender():
    return faker.random_element(WRONG_EMAILS)

def getWrongPhoneNumber():
    return '123a123a'

def getWrongCreaditCard():
    return 'WRONGWRONG'

wrongFuncMap = {
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
    userData.weight = faker.random_int(min=50, max=200)
    userData.height = faker.random_int(min=50, max=200)

    return userData

def getWrongUserData():
    userData = UserRaw()
    userData.name = faker.name()
    userData.age = faker.random_int(min= 5, max= 100)
    userData.gender = faker.random_element(GENDERS)
    userData.email = faker.random_element(WRONG_EMAILS)
    userData.phoneNumber = faker.phone_number()
    userData.address = faker.address()
    userData.creditCardId = faker.credit_card_number()
    userData.weight = faker.random_int(min=50, max=200)
    userData.height = faker.random_int(min=50, max=200)

    # Overwrite some wrong data
    randomObjects = faker.random_choices(list(wrongFuncMap.items()))
    for property, getterWrongData in randomObjects:
        setattr(userData, property, getterWrongData())
    
    return userData

def getWrongGenderOnly():
    data = getRightUserData()
    data.gender = None
    return data


def getRandomUserData():
    if (faker.random_int(min=0, max=100) < 40):
        return getWrongUserData()
    return getRightUserData()

def getListRandomUserData(number=5):
    list_rs = []
    for i in range(number):
        list_rs.append(getRandomUserData())
    return list_rs