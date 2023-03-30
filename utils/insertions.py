from bson import ObjectId


from utils.utils import get_collection, hash_password
from utils.utils import generate_session_id


def insert_user(user_info):
    """!@brief Insert a new user into the database"""
    collection = get_collection("users")
    user_info.password = hash_password(user_info.password)
    collection.insert_one(user_info.dict())


def insert_session(user_id, session_info) -> str:
    """!@brief Insert a new session into the database
        @return session_id"""
    collection = get_collection("sessions")
    session_id = generate_session_id(user_id, session_info.login_time, session_info.machine_id)
    collection.insert_one({"session_id": session_id,
                           "user_id": user_id,
                           "login_time": session_info.login_time,
                           "machine_id": session_info.machine_id})
    return session_id


def insert_post(post_info):
    """!@brief Insert posts into the database"""
    collection = get_collection("posts")
    result = collection.insert_one(post_info.dict())
    return result.acknowledged


def insert_comment(id_val: str, comment):
    post_query = {'_id': ObjectId(id_val)}
    new_value = {'$push': {'comments': comment.dict(by_alias=True, exclude_unset=True)}}
    collection = get_collection("posts")
    result = collection.update_one(post_query, new_value)
    return result.modified_count



