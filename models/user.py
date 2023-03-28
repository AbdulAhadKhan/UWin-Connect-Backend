from fastapi import UploadFile
from pydantic import BaseModel, Field, BaseConfig
from typing import Union
from bson import ObjectId

from utils.helpers import form, ObjectID
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


class UserMinResponse(UserMin):
    id: str


class Registration(UserMin):
    password: str
    gender: str


class UserFull(UserMin):
    role: Union[Role, None] = None
    description: Union[str, None] = None
    image: Union[UploadFile, None] = None


class UserFullResponse(UserFull):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

    id: ObjectID = Field(..., alias="_id")
    image: Union[str, None] = None


class UserUpdate(BaseModel):
    firstname: str
    lastname: str
    description: Union[str, None] = None
    image: Union[str, None] = None
