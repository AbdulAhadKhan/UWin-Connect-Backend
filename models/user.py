from pydantic import BaseModel
from typing import Union
from .session import NewSession

class Login(BaseModel):
    email: str
    password: str
    meta: NewSession

class Role(BaseModel):
    title: str
    department: Union[str, None] = None
    designation: Union[str, None] = None

class User(BaseModel):
    email: str
    firstname: str
    lastname: str
    role: Role

class Registration(User):
    password: str
    gender: str
