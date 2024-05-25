import json
from prefect import flow, task
from model.user_modal_post import UserModelPost
from model.user_raw_model import UserRaw
from utils.db import (
    get_incorrect_data,
    save_correct_data,
    save_failed_data,
    delete_incorrect_data
)

@task
def get_incorrect_user_data():
    rs = get_incorrect_data()
    print('RAW DATA:', rs)
    return rs

@task(retries=1, retry_delay_seconds=1)
def validate_userData(userTupple):
    print('RAW USER: ', userTupple)

    userJson = {
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
    is_success = False
    try:
        userData = UserModelPost(**userJson)
        is_success = True
    except Exception as e:
        print('FAILED to parse: ', userTupple, e)
        userData = UserRaw(**userJson)
        is_success = False
    print('Success: ', is_success , ' - PARSED USER: ', userData)

    return is_success, userTupple, userData

@task
def validate_input(input):
    print('PROCESS - validate user: ', input)
    list_correct_data = []
    list_failed_data = []

    list_future = validate_userData.map(input)

    for future_rs in list_future:
        is_success, userTupple, userData = future_rs.result()
        if is_success:
            list_correct_data.append((userTupple, userData))
        else:
            list_failed_data.append((userTupple, userData))

    return list_correct_data, list_failed_data

@task(retries=1, retry_delay_seconds=2)
def send_to_db(input):
    listUserData = [t[1] for t in input]
    listUserTupple = [t[0] for t in input]
    print('SUCCESS - save to db', listUserData)
    save_correct_data(listUserData)
    return listUserTupple


@task(retries=1, retry_delay_seconds=2)
def send_to_fail_db(input):
    listUserData = [t[1] for t in input]
    listUserTupple = [t[0] for t in input]
    print('FAILED - User raw json data: ', listUserData)
    save_failed_data(listUserData)
    return listUserTupple

@task(retries=1, retry_delay_seconds=2)
def remove_incorrect_data(input):
    delete_incorrect_data(input)

@flow(log_prints=True)
def user_fix_pipeline():
    userTupple = get_incorrect_user_data()
    list_correct_data,  list_failed_data = validate_input(userTupple)
    future_db = send_to_db.submit(list_correct_data)
    future_incorrect_db = send_to_fail_db.submit(list_failed_data)
    list_corect = future_db.result()
    list_failed = future_incorrect_db.result()
    remove_incorrect_data.submit(list_corect)
    remove_incorrect_data.submit(list_failed)