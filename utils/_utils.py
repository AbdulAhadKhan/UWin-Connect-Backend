import yaml
from argon2 import PasswordHasher, exceptions
from pymongo import MongoClient

CONFIGS = yaml.safe_load(open("utils/dev-config.yml"))

def get_collection(collection_name) -> MongoClient:
    assert collection_name in CONFIGS['collections'], f'Collection "{collection_name}" not found'
    client = MongoClient(CONFIGS['atlas_uri'])
    return client[CONFIGS['db']][CONFIGS['collections'][collection_name]]

def hash_password(password: str) -> str:
    """!@brief Hash a password using Argon2."""
    password_hasher = PasswordHasher()
    return password_hasher.hash(password)

def compare_hashed_password(password: str, hashed_password: str) -> bool:
    """!@brief Verify a password using Argon2."""
    password_hasher = PasswordHasher()
    try:
        return password_hasher.verify(hashed_password, password)
    except exceptions.VerifyMismatchError:
        return False