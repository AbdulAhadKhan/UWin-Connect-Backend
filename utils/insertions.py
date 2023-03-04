from ._utils import get_collection, hash_password

def insert_user(user_info):
    """!@brief Insert a new user into the database"""
    collection = get_collection("users")
    user_info.password = hash_password(user_info.password)
    collection.insert_one(user_info.dict())
