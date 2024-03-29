from utils.utils import get_collection, hash_password
from utils.utils import generate_session_id, clean_dict


async def insert_user(user_info):
    """!@brief Insert a new user into the database"""
    collection = get_collection("users")
    user_info.password = hash_password(user_info.password)
    collection.insert_one(user_info.dict())


async def insert_session(user_id, session_info) -> str:
    """!@brief Insert a new session into the database
        @return session_id"""
    collection = get_collection("sessions")
    session_id = generate_session_id(
        user_id, session_info.login_time, session_info.machine_id)
    collection.insert_one({"session_id": session_id,
                           "user_id": user_id,
                           "login_time": session_info.login_time,
                           "machine_id": session_info.machine_id})
    return session_id


async def insert_post(post_info):
    """!@brief Insert posts into the database"""
    collection = get_collection("posts")
    post_info = clean_dict(post_info.dict())
    result = collection.insert_one(post_info)
    return result.acknowledged
