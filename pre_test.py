from generator.user_generator import (
    getListRandomUserData,
    getWrongGenderOnly,
    getRandomTrueFalse
)
from pre_flow import user_pipeline
from utils.hash import hash_text
import json

if __name__ == '__main__':
    input_data = getListRandomUserData(15)
    input_data.append(getWrongGenderOnly())
    input_data.append(getWrongGenderOnly())
    input_data.append(getWrongGenderOnly())

    payload = []
    for userData in input_data:
        hashed = hash_text(json.dumps(userData,default=lambda x: x.dict()))
        if getRandomTrueFalse(25):
            hashed = 'WRONG_HASHED'
        payload.append({
            'hashed': hashed,
            'data': userData
        })

    print('INPUT DATA: ', payload)
    user_pipeline(json.dumps(payload, default=lambda x: x.dict()))