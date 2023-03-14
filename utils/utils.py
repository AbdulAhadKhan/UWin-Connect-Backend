import yaml
import certifi

from time import time
from argon2 import PasswordHasher, exceptions
from hashlib import sha256
from pymongo import MongoClient
from fastapi import UploadFile

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

def hash_file_name(file_name: str) -> str:
    """!@brief Hash a file name with time as a salt"""
    return sha256(f"{file_name}{time()}".encode('utf-8')).hexdigest()

def get_file(file_name: str) -> bytes:
    """!@brief Get a file from a bucket"""
    with open(f".data/{file_name}", 'rb') as f:
        return f.read()

async def store_file(meta: UploadFile) -> str:
    """!@brief Upload a file to a bucket"""
    extension = meta.filename.split('.')[-1]
    file_name = f"{hash_file_name(meta.filename)}.{extension}"
    with open(f".data/{file_name}", 'wb') as f:
        f.write(await meta.read())
    return file_name
