from minio import Minio
import io

HOST_PORT = "192.168.237.2:9000"
ACCESS_KEY = "Hfy4wcXuVhEPgL3GI1zf"
ACCESS_SECRET = "iAaThhrOemUhVodqAhr0EvxSA3ZfJAdZRcClRaZ5"

SOURCE_BUCKET = "source-bucket"
DESTINATION_BUCKET = "destination-bucket"

def list_source_objects():
    client = Minio(
        HOST_PORT,
        ACCESS_KEY,
        ACCESS_SECRET,
        secure=False
    )

    list_objects = client.list_objects(SOURCE_BUCKET)
    rs = []
    for obj in list_objects:
        rs.append(obj.object_name)
    return rs

def get_source_object(key):
    client = Minio(
        HOST_PORT,
        ACCESS_KEY,
        ACCESS_SECRET,
        secure=False
    )

    try:
        response = client.get_object(SOURCE_BUCKET, key)
        # Read data from response.
        print(response)
        print(response.getheader('etag'))
        print(response.getheaders())
        return response.data, response.getheader('etag')
    except Exception as e:
        print(e)
    finally:
        response.close()
        response.release_conn()

def put_destination_object(data, key):
    client = Minio(
        HOST_PORT,
        ACCESS_KEY,
        ACCESS_SECRET,
        secure=False
    )
    
    result = client.put_object(
        DESTINATION_BUCKET, key, io.BytesIO(data), length=len(data),
    )
    print(
    "created {0} object; etag: {1}, version-id: {2}".format(
            result.object_name, result.etag, result.version_id,
        ),
    )
    return result