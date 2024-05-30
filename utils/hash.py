import hashlib

def hash_text(jsonData: str):
    """
        Basic hashing function for a text using random unique salt.  
    """
    return hashlib.sha256(jsonData.encode()).hexdigest()
    
def match_hashed_text(hashedText: str, jsonData: str):
    """
        Check for the text in the hashed text
    """
    return hashedText == hashlib.sha256(jsonData.encode()).hexdigest()

def calculate_s3_etag_from_path(file_path, chunk_size=8 * 1024 * 1024):
    md5s = []

    with open(file_path, 'rb') as fp:
        while True:
            if chunk_size > 0:
                data = fp.read(chunk_size)
            else:
                data = fp.read()
            if not data:
                break
            md5s.append(hashlib.md5(data))

    if len(md5s) < 1:
        return '"{}"'.format(hashlib.md5().hexdigest())

    if len(md5s) == 1:
        return '"{}"'.format(md5s[0].hexdigest())

    digests = b''.join(m.digest() for m in md5s)
    digests_md5 = hashlib.md5(digests)
    return '"{}-{}"'.format(digests_md5.hexdigest(), len(md5s))

def calculate_s3_etag(data):
    return '"{}"'.format(hashlib.md5(data).hexdigest())