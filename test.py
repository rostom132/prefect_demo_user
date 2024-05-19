from model.user_modal_pre import UserModelPre
from model.user_raw_model import UserRaw
from utils.saver import save_incorrect_data

if __name__ == '__main__':
    # inputData = {
    #     'height': 50,
    #     'weight': 150
    # }
    # rs = auto_correct('gender', None, inputData)
    # print('Result is ', rs)

    input_data = {
        "name": "Kelly Zuniga",
        "gender": "weak",
        "age": 18,
        "email": "uvazquez@gmail1.com",
        "phoneNumber": "528.365.9480",
        "address": "Unit 1851 Box 0909\nDPO AA 70681",
        "creditCardId": "341053990308816",
        "height": 50,
        "weight": 100
    }
    print('RAW USER:', input_data)

    user = UserModelPre(**input_data)
    save_incorrect_data([user])

    print('FULL USER:', user)