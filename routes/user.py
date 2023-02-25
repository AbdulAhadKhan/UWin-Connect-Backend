from fastapi import APIRouter
from pydantic import BaseModel
from models.user import User 
from config.db import conn 
from schemas.user import serializeDict, serializeList
from bson import ObjectId
user = APIRouter() 
class UserModel(BaseModel):
    userid: str              
    password: str

@user.get('/GetallUser/')
async def find_all_users():
    return serializeList(conn.UWinsuccess.myTable.find())

@user.get('/GetuserById/{id}')
async def find_one_user(id):  
    return serializeDict(conn.UWinsuccess.myTable.find_one({"userid":"1"}))

@user.post('/Register/')
async def create_user(user: User):
    conn.UWinsuccess.myTable.insert_one(dict(user))
    return serializeList(conn.UWinsuccess.myTable.find())

@user.put('/UpdateUserProfile/{id}')
async def update_user(id,user: User):
    conn.UWinsuccess.myTable.find_one_and_update({"userid":id},{
        "$set":dict(user)
    })
    return serializeDict(conn.UWinsuccess.myTable.find_one({"userid":ObjectId(id)}))

@user.delete('/DeleteUser/{id}')
async def delete_user(id,user: User):
    return serializeDict(conn.UWinsuccess.myTable.find_one_and_delete({"userid":id}))

@user.post("/Login/")
def user_Login(user: UserModel):  
    cursor=conn.UWinsuccess.myTable.find_one({"userid":user.userid,
                                 "password":user.password})
    if cursor==None:
        return "INVALID USERNAME OR PASSWORD"
    else :
       return 1
    

