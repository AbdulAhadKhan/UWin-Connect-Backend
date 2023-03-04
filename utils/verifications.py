import os
from pymongo import MongoClient

COLLECTION_MAP = {
    "user": "USER_COLLECTION",
}

def get_collection(collection_name) -> MongoClient:
    assert collection_name in COLLECTION_MAP, f'Collection "{collection_name}" not found'
    client = MongoClient(os.environ.get("ATLAS_URL"))
    return client[os.environ.get("DB")][os.environ.get("USER_COLLECTION")]

def email_exists(email) -> bool:
    collection = get_collection("user")
    return collection.find_one({"email": email}) is not None
