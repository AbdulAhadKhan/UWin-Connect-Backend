import yaml
from pymongo import MongoClient

CONFIGS = yaml.safe_load(open("utils/dev-config.yml"))

def get_collection(collection_name) -> MongoClient:
    assert collection_name in CONFIGS['collections'], f'Collection "{collection_name}" not found'
    client = MongoClient(CONFIGS['atlas_uri'])
    return client[CONFIGS['db']][CONFIGS['collections'][collection_name]]