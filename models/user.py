from fastapi import UploadFile
from pydantic import BaseModel
from typing import Union

from utils.helpers import form
from models.session import NewSession

class Login(BaseModel):
    email: str
    password: str
    meta: NewSession

class Role(BaseModel):
    title: str
    department: Union[str, None] = None
    designation: Union[str, None] = None

class UserMin(BaseModel):
    email: str
    firstname: str
    lastname: str
    role: Role

class Registration(UserMin):
    password: str
    gender: str

# TODO: Remove role override
@form
class UserFull(UserMin):
    role: Union[Role, None] = None
    description: Union[str, None] = None
    image: Union[UploadFile, None] = None
