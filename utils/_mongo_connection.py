import os
from pymongo import MongoClient

COLLECTION_MAP = {
    "user": "USER_COLLECTION",
}

def get_collection(collection_name) -> MongoClient:
    assert collection_name in COLLECTION_MAP, f'Collection "{collection_name}" not found'
    client = MongoClient(os.environ.get("ATLAS_URI"))
    return client[os.environ.get("DB")][os.environ.get(COLLECTION_MAP[collection_name])]
