from utils.hash import calculate_s3_etag
from utils.minio_client import (
    get_source_object,
    list_source_objects,
    put_destination_object
)
from model.constants import Gender

if __name__ == '__main__':
    print(Gender.has_value('male'))
    print(Gender.has_value('asda'))
    if Gender.has_value('male'):
        print('YES')
    if Gender.has_value('mae'):
        print('DASDASD')
    # filepath = './Asdasd.png'
    # print(calculate_s3_etag(filepath, -1))
    # data, etag = get_source_object('Asdasd.png')
    # print(data)
    # print(etag)
    # list_source_objects()
    # put_destination_object('New.png', data)