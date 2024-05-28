from generator.user_generator import (
    getListRandomUserData,
    getWrongGenderOnly
)
from pre_flow import user_pipeline_structured
from utils.db import (
    save_source_data
)

if __name__ == '__main__':
    input_data = getListRandomUserData(15)
    input_data.append(getWrongGenderOnly())
    input_data.append(getWrongGenderOnly())
    input_data.append(getWrongGenderOnly())

    print('INPUT DATA: ', input_data)
    save_source_data(input_data)

    user_pipeline_structured()