from pydantic import BaseModel
from typing import Union
from .session import NewSession

class Login(BaseModel):
    email: str
    password: str
    meta: NewSession

class Faculty(BaseModel):
    department: str
    designation: str

class Registration(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    role: Union[str, Faculty]
    gender: str
