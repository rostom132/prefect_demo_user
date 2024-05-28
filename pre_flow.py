import json
from prefect import flow, task
from model.user_modal_pre import UserModelPre
from model.user_raw_model import UserRaw
from utils.db import (
    save_correct_data,
    save_incorrect_data,
    get_source_data,
    delete_source_data
)
from utils.hash import (
    match_hashed_text
)
from model.constants import DataType

@task
def load_data_to_json(input: str):
    print('LOAD JSON - user data: ', input)
    return json.loads(input)

@task
def load_data_from_db_source():
    rs = get_source_data()
    print('RAW DATA:', rs)
    return rs

@task
def convert_source_data(input):
    print('convert_source_data - validate user: ', input)
    list_future = tupple_to_dict.map(input)

    rs = []

    for future_rs in list_future:
        rs.append(future_rs.result())

    return rs

@task
def tupple_to_dict(userTupple):
    userDict = {
        'name': userTupple[1],
        'age': userTupple[2],
        'gender': userTupple[3],
        'email': userTupple[4],
        'phoneNumber': userTupple[5],
        'address': userTupple[6],
        'creditCardId': userTupple[7],
        'weight': userTupple[8],
        'height': userTupple[9],
    }
    return userDict

@task
def all_integrity_check(allUserJson):
    list_data = []
    list_corupted_data = []

    list_future = integrity_check.map(allUserJson)
    for future_rs in list_future:
        is_integrity, userData = future_rs.result()
        if is_integrity:
            list_data.append(userData)
        else:
            list_corupted_data.append(userData)

    return list_data, list_corupted_data

@task
def integrity_check(userJson):
    try:
        hashed = userJson['hashed']
        text = json.dumps(userJson['data'],default=lambda x: x.dict())
        if match_hashed_text(hashed, text):
            return True, userJson['data']
    except Exception as e:
        print('FAILED to check integrity: ', userJson['data'], e)
    return False, userJson['data']

@task
def validate_input(allUsersData):
    print('PROCESS - validate user: ', allUsersData)
    list_correct_data = []
    list_incorrect_data = []
    list_corupted_data = []

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

@task
def validate_userData(userJson):
    print('RAW USER: ', userJson)
    type_of_data = DataType.corrupted

    try:
        userData = UserModelPre(**userJson)
        type_of_data = DataType.correct
    except Exception as e:
        print('FAILED to parse: ', userJson, e)
        userData = UserRaw(**userJson)
        type_of_data = DataType.incorrect
    print('PARSED USER: ', userData)

    return type_of_data, userData

@task(retries=1, retry_delay_seconds=2)
def send_to_db(listUserData: UserModelPre):
    print('CORRECT - save to db', listUserData)
    save_correct_data(listUserData)

@task(retries=1, retry_delay_seconds=2)
def send_to_incorrect_db(listUserData: str):
    print('INCORRECT - User raw json data: ', listUserData)
    save_incorrect_data(listUserData)

@task(retries=1, retry_delay_seconds=2)
def remove_source_data(input):
    delete_source_data(input)

@task(retries=1, retry_delay_seconds=2)
def handle_corrupted_data(userJson):
    print('CORRUPTED DATA - User raw json data: ', userJson)

## FLOWS
@flow(log_prints=True)
def user_pipeline_semi_structured(userJsonDatas: str = "[]"):
    all_user_data = load_data_to_json(userJsonDatas)
    all_user_data, list_corupted_data = all_integrity_check(all_user_data)
    list_correct_data, list_incorrect_data, new_list_corupted_data = validate_input(all_user_data)
    send_to_db.submit(list_correct_data)
    send_to_incorrect_db.submit(list_incorrect_data)
    handle_corrupted_data.submit(list_corupted_data + new_list_corupted_data)


@flow(log_prints=True)
def user_pipeline_structured():
    raw_data = load_data_from_db_source()
    all_user_data = convert_source_data(raw_data)
    list_correct_data, list_incorrect_data, list_corupted_data = validate_input(all_user_data)
    send_to_db.submit(list_correct_data)
    send_to_incorrect_db.submit(list_incorrect_data)
    handle_corrupted_data.submit(list_corupted_data)
    remove_source_data(raw_data)