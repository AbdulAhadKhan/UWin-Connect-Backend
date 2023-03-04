from pydantic import BaseModel
from typing import Union

class Login(BaseModel):
    email: str
    password: str

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
