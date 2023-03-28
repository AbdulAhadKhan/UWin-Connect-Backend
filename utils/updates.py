from utils.utils import get_collection, clean_dict


async def update_user(email, data):
    """!@brief Update a user in the database"""
    collection = get_collection('users')
    data = clean_dict(dict(data))

    document = collection.update_one(
        {"email": email}, {"$set": data})
    if document.matched_count == 0:
        raise Exception("User not updated")
