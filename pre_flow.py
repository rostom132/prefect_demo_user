import json
from prefect import flow, task
from model.user_modal_pre import UserModelPre
from model.user_raw_model import UserRaw
from utils.db import (
    save_correct_data,
    save_incorrect_data
)

@task(retries=1, retry_delay_seconds=1)
def validate_userData(userJson):
    print('RAW USER: ', userJson)
    is_success = False
    try:
        userData = UserModelPre(**userJson)
        is_success = True
    except Exception as e:
        print('FAILED to parse: ', userJson, e)
        userData = UserRaw(**userJson)
        is_success = False
    print('PARSED USER: ', userData)

    return is_success, userData

@task
def validate_input(input: str):
    print('PROCESS - validate user: ', input)
    list_correct_data = []
    list_failed_data = []

    allUsersData = json.loads(input)
    list_future = validate_userData.map(allUsersData)

    for future_rs in list_future:
        is_success, userData = future_rs.result()
        if is_success:
            list_correct_data.append(userData)
        else:
            list_failed_data.append(userData)

    return list_correct_data, list_failed_data

@task(retries=1, retry_delay_seconds=2)
def send_to_db(listUserData: UserModelPre):
    print('SUCCESS - save to db', listUserData)
    save_correct_data(listUserData)
    return None


@task(retries=1, retry_delay_seconds=2)
def send_to_fail_db(listUserData: str):
    print('FAILED - User raw json data: ', listUserData)
    save_incorrect_data(listUserData)
    return None

@flow(log_prints=True)
def user_pipeline(userJsonDatas: str = "[]"):
    list_correct_data,  list_failed_data = validate_input(userJsonDatas)
    send_to_db.submit(list_correct_data)
    send_to_fail_db.submit(list_failed_data)