import json
from prefect import flow, task
from model.user_modal_pre import UserModelPre

@task(retries=2)
def validate_input(input: str):
    print('PROCESS - validate user: ', input)
    userJson = json.loads(input)
    userData = UserModelPre(**userJson)
    return userData

@task(retries=3, retry_delay_seconds=3)
def send_to_db(userData: UserModelPre):
    print('SUCCESS - save to db', userData)

@task(retries=3, retry_delay_seconds=3)
def send_to_fail_db(userJsonData: str, exception):
    print('FAILED - User raw json data: ', userJsonData)
    print('FAILED - Exception: ', exception)


@flow(log_prints=True)
def user_pipeline(userJsonData: str = "{}"):
    try:
        userData = validate_input(userJsonData)
    except Exception as e:
        send_to_fail_db(userJsonData, e)
    else:
        send_to_db(userData)

if __name__ == "__main__":
    user_pipeline.deploy(
        name="user-pipeline-image-deployment", 
        work_pool_name="intern_demo"
    )