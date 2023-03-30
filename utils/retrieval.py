from utils.utils import get_collection
import pymongo
from datetime import datetime

async def fetch_posts(name: str):
    filter = {"userid": name}
    collection = get_collection("posts")
    posts = collection.find(filter, {"userid": name})
    posts = str(list(posts))
    return posts

async def fetch_user(name: str) -> dict:
    collection = get_collection("users")
    return collection.find_one({"email": name}, {"password": 0})



async def getother_posts(user_id: str, last_time: int):
    # last_time = datetime.strptime(last_time, "%Y%m%d")
    print(last_time)
    collection = get_collection("posts")
    cursor = collection.find({"userid": {"$ne": user_id}, 
                              "timestamp": {"$lt": last_time}}).sort("timestamp", 
                                                                     pymongo.DESCENDING).limit(10)
    entries = cursor[:]
    return list(entries)