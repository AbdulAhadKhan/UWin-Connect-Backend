# from fastapi import FastAPI, Request
#
# app = FastAPI()
#
# @app.get("/echo")
# async def get_item(request: Request):
#     return await request.json()


from typing import Union
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import FastAPI

DB="QLeap"
USER_COLLECTION="users"


class UserModel(BaseModel):
    username: str
    password: str
    email: str

app = FastAPI()


@app.post("/register")
def user_register(user: UserModel):
    print("debug",user)
    with MongoClient() as client:
        collection = client[DB][USER_COLLECTION]
        result = collection.insert_one(user.dict())
        ack = result.acknowledged
        return {"insertion": ack}