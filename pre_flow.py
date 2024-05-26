import json
from prefect import flow, task
from model.user_modal_pre import UserModelPre
from model.user_raw_model import UserRaw
from utils.db import (
    save_correct_data,
    save_incorrect_data
)
from utils.hash import (
    match_hashed_text
)
from model.constants import DataType

@task
def integrity_check(userJson):
    try:
        hashed = userJson['hashed']
        text = json.dumps(userJson['data'],default=lambda x: x.dict())
        if match_hashed_text(hashed, text):
            return True
    except Exception as e:
        print('FAILED to check integrity: ', userJson['data'], e)
    return False

@task
def validate_userData(userJson):
    print('RAW USER: ', userJson)
    type_of_data = DataType.corrupted
    
    if not integrity_check(userJson):
        return type_of_data, userJson

    try:
        userData = UserModelPre(**userJson['data'])
        type_of_data = DataType.correct
    except Exception as e:
        print('FAILED to parse: ', userJson['data'], e)
        userData = UserRaw(**userJson['data'])
        type_of_data = DataType.incorrect
    print('PARSED USER: ', userData)

    return type_of_data, userData

@task
def validate_input(input: str):
    print('PROCESS - validate user: ', input)
    list_correct_data = []
    list_incorrect_data = []
    list_corupted_data = []

    allUsersData = json.loads(input)
    list_future = validate_userData.map(allUsersData)

    for future_rs in list_future:
        type_of_data, userData = future_rs.result()
        if type_of_data == DataType.correct:
            list_correct_data.append(userData)
        if type_of_data == DataType.incorrect:
            list_incorrect_data.append(userData)
        if type_of_data == DataType.corrupted:
            list_corupted_data.append(userData)

    return list_correct_data, list_incorrect_data, list_corupted_data

@task(retries=1, retry_delay_seconds=2)
def send_to_db(listUserData: UserModelPre):
    print('CORRECT - save to db', listUserData)
    save_correct_data(listUserData)


@task(retries=1, retry_delay_seconds=2)
def send_to_incorrect_db(listUserData: str):
    print('INCORRECT - User raw json data: ', listUserData)
    save_incorrect_data(listUserData)

@task(retries=1, retry_delay_seconds=2)
def handle_corrupted_data(userJson):
    print('CORRUPTED DATA - User raw json data: ', userJson)

@flow(log_prints=True)
def user_pipeline(userJsonDatas: str = "[]"):
    list_correct_data, list_incorrect_data, list_corupted_data = validate_input(userJsonDatas)
    send_to_db.submit(list_correct_data)
    send_to_incorrect_db.submit(list_incorrect_data)
    handle_corrupted_data.submit(list_corupted_data)