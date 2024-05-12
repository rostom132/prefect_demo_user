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


@flow(log_prints=True)
def user_pipeline(userJsonData: str = "{}"):
    userData = None
    try:
        userData = validate_input(userJsonData)
    except:
        print('DEAD')
    
    send_to_db(userData)

if __name__ == "__main__":
    user_pipeline.deploy(
        name="user-pipeline-image-deployment", 
        work_pool_name="intern_demo"
    )