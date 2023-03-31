from bson import ObjectId

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


def push_like(email, post_id):
    """!@brief Add a like to a post"""
    collection = get_collection("posts")
    post_id = ObjectId(post_id)
    document = collection.update_one({"_id": post_id}, {
        "$addToSet": {"likes": email}})
    if document.matched_count == 0:
        raise Exception("Like not added")


def pop_like(email, post_id):
    """!@brief Remove a like from a post"""
    collection = get_collection("posts")
    post_id = ObjectId(post_id)
    document = collection.update_one({"_id": post_id}, {
        "$pull": {"likes": email}})
    if document.matched_count == 0:
        raise Exception("Like not removed")
