from typing import Union

from dotenv import dotenv_values
from fastapi import Request
from pydantic import BaseModel, validator
from pydantic.fields import Optional, Field
from pymongo import MongoClient
from fastapi import FastAPI


# config = dotenv_values(".env")


DB = "QLeap"
USER_COLLECTION = "users"


class UserModel(BaseModel):
    select: str
    role: Optional[str]
    course: Optional[str]
    # username: str
    firstname: str
    lastname: str
    email: str
    password: str
    gender: str
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    description: Optional[str]


    # @validator(email)
    # def validate_email(cls, v):
    #     if MongoClient()[DB][USER_COLLECTION].find_one({'email': v}):
    #         raise ValueError('Email already exists')
    #     # Check if email is unique
    #     # You can use any database or ORM to check for duplicates
    #     return v


app = FastAPI()


@app.get("/echo")
async def get_item(request:Request):
    return await request.json()


def verify_username_email(data, client):
    # collection = client[DB][USER_COLLECTION]
    # records = collection.find()
    # print(records)
    pass




@app.post("/register", status_code=201)
async def user_register(user: UserModel):

    print("debug",user)
    with MongoClient() as client:
    # with MongoClient(config["ATLAS_URI"]) as client:
        try:
            verify_username_email(user.dict(), client)
        except:
            return {"status": "username or password already exists"}
        collection = client[DB][USER_COLLECTION]
        result = collection.insert_one(user.dict())
        ack = result.acknowledged
        return {"insertion": ack}


@app.put("/updateprofile", status_code=201)
async def edit_user_profile(user: UserModel):
    record = user.dict()
    email = record["email"]

    filter = {"email": email}
    update = {"$set": record}
    with MongoClient() as client:
        collection = client[DB][USER_COLLECTION]
        collection.update_one(filter, update)

    return {"message": "User profile updated successfully"}
    # else:
    #     return {"message": f"User {email} not found"}