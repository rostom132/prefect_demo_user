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