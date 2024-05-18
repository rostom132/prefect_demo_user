import json
from prefect import flow, task
from model.user_model import UserModel

@task(retries=2)
def validate_input(input: str):
    userJson = json.loads(input)
    userData = UserModel(**userJson)
    return userData

@task
def send_to_db(userData: UserModel):
    print(userData)

@task
def send_to_fail_db(userJsonData: str, exception):
    print('User raw json data: ', userJsonData)
    print('Exception: ', exception)


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