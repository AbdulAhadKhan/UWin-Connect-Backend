from utils.utils import get_collection
import pymongo
from datetime import datetime


async def fetch_n_posts_by_user_le_time(email: str, next_timestamp: str, page_size: int):
    collection = get_collection("posts")
    result = collection.aggregate([
        {
            "$sort": {
                "timestamp": 1
            }
        },
        {
            "$match": {
                "email": email,
                "timestamp": {
                    "$gt": next_timestamp
                }
            }
        },
        {
            "$limit": page_size
        },
        {
            "$project": {
                "_id": {
                    "$toString": "$_id"
                },
                "email": 1,
                "description": 1,
                "timestamp": 1,
                "image": 1
            }
        }
    ])
    posts = list(result)
    last_timestamp = posts[-1]["timestamp"] if posts else None

    return posts, last_timestamp


async def fetch_user(name: str) -> dict:
    collection = get_collection("users")
    return collection.find_one({"email": name}, {"password": 0})


async def getother_posts(user_id: str, last_time: str):
    last_time = datetime.strptime(last_time, "%Y%m%d")
    print(last_time)
    collection = get_collection("posts")
    cursor = collection.find({"userid": {"$ne": user_id},
                              "timestamp": {"$lt": last_time}}).sort("timestamp",
                                                                     pymongo.DESCENDING).limit(10)
    entries = cursor[:]
    return list(entries)
