import json
from prefect import flow, task
from model.user_modal_pre import UserModelPre
from model.user_raw_model import UserRaw

@task(retries=2)
def validate_input(input: str):
    print('PROCESS - validate user: ', input)
    list_correct_data = []
    list_failed_data = []

    allUsersData = json.loads(input)
    for userJson in allUsersData:
        try:
            userData = UserModelPre(**userJson)
            list_correct_data.append(userData)
        except Exception as e:
            print('FAILED to parse: ', userJson, e)
            userData = UserRaw(**userJson)
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