from generator.user_generator import (
    getListRandomUserData,
    getWrongGenderOnly
)
from pre_flow import user_pipeline
import json

if __name__ == '__main__':
    input_data = getListRandomUserData(20)
    input_data.append(getWrongGenderOnly())
    input_data.append(getWrongGenderOnly())
    input_data.append(getWrongGenderOnly())
    print('INPUT DATA: ', input_data)
    user_pipeline(json.dumps(input_data, default=lambda x: x.dict()))