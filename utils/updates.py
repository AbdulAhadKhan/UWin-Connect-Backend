from utils.utils import get_collection, clean_dict


async def update_user(email, data):
    """!@brief Update a user in the database"""
    collection = get_collection('users')
    data = clean_dict(dict(data))

    document = collection.update_one(
        {"email": email}, {"$set": data})
    if document.matched_count == 0:
        raise Exception("User not updated")


def push_friend(email, friend_email):
    """!@brief Add a friend to a user"""
    collection = get_collection("users")
    document = collection.update_one({"email": email}, {
        "$addToSet": {"friends": friend_email}})
    if document.matched_count == 0:
        raise Exception("Friend not added")


def pop_friend(email, friend_email):
    """!@brief Remove a friend from a user"""
    collection = get_collection("users")
    document = collection.update_one({"email": email}, {
        "$pull": {"friends": friend_email}})
    if document.matched_count == 0:
        raise Exception("Friend not removed")
