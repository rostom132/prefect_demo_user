import json
from prefect import flow, task
from model.user_modal_pre import UserModelPre
from model.user_raw_model import UserRaw

@task(retries=2, retry_delay_seconds=3)
def validate_userData(userJson):
    is_success = False
    try:
        userData = UserModelPre(**userJson)
        is_success = True
    except Exception as e:
        print('FAILED to parse: ', userJson, e)
        userData = UserRaw(**userJson)
        is_success = False
    
    return is_success, userData

@task(retries=2)
def validate_input(input: str):
    print('PROCESS - validate user: ', input)
    list_correct_data = []
    list_failed_data = []

    allUsersData = json.loads(input)
    list_rs = validate_userData.map(allUsersData)

    for is_success, userData in list_rs:
        if is_success:
            list_correct_data.append(userData)
        else:
            list_failed_data.append(userData)

    return list_correct_data, list_failed_data

@task(retries=3, retry_delay_seconds=3)
def send_to_db(listUserData: UserModelPre):
    print('SUCCESS - save to db', listUserData)

@task(retries=3, retry_delay_seconds=3)
def send_to_fail_db(listUserData: str):
    print('FAILED - User raw json data: ', listUserData)


@flow(log_prints=True)
def user_pipeline(userJsonDatas: str = "[]"):
    list_correct_data,  list_failed_data = validate_input(userJsonDatas)
    send_to_db(list_correct_data)
    send_to_fail_db(list_failed_data)