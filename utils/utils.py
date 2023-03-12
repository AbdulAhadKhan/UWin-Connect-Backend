import yaml
import certifi

from argon2 import PasswordHasher, exceptions
from hashlib import sha256
from pymongo import MongoClient

CONFIGS = yaml.safe_load(open("utils/dev-config.yml"))

def get_collection(collection_name: str) -> MongoClient:
    assert collection_name in CONFIGS['collections'], f'Collection "{collection_name}" not found'
    client = MongoClient(CONFIGS['atlas_uri'], tlsCAFile=certifi.where())
    return client[CONFIGS['db']][CONFIGS['collections'][collection_name]]

def clean_dict(dictionary: dict) -> dict:
    """!@brief Remove all None values from a dictionary"""
    return {k: v for k, v in dictionary.items() if v is not None}

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
    
def generate_session_id(user_id, login_time: str, machine_id: str) -> str:
    """!@brief Create a new session for a user
        @return session_id"""
    session_id = sha256(f"{user_id}{login_time}{machine_id}".encode('utf-8')).hexdigest()
    return session_id
