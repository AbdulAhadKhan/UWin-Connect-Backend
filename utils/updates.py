from utils.utils import get_collection, clean_dict

async def update_user(user_info):
    """!@brief Update a user in the database"""
    collection = get_collection('users')
    user_info = clean_dict(user_info.dict())

    document = collection.update_one({"email": user_info['email']}, {"$set": user_info})
    if document.matched_count == 0: raise Exception("User not updated")
