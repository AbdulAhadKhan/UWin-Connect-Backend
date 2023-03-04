from fastapi import Request, Response
from fastapi import FastAPI, status

from utils.verifications import email_exists, verify_password
from utils.insertions import insert_user, insert_session
from models.user import Registration, Login

app = FastAPI()


@app.get("/echo")
async def echo(request: Request):
    """Echo the request body as JSON"""
    return await request.json()


@app.post("/register", status_code=201, responses={201: {"description": "User created successfully"},
                                                   422: {"description": "Email already exists"}})
async def register(user_info: Registration, response: Response):
    """Register a new user"""

    # Check if email already exists
    if email_exists(user_info.email):
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"message": "Email already exists"}
    
    # Insert user into database
    insert_user(user_info)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "User created successfully"}


@app.get("/login", status_code=200, responses={200: {"description": "Login successful"},
                                               401: {"description": "Invalid credentials"}})
async def login(user: Login, response: Response):
    if email_exists(user.email) and verify_password(user.email, user.password):
        session_id = insert_session(user.email, user.meta)
        return {"message": "Login successful", "session_id": session_id}
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"message": "Invalid credentials"}


@app.put("/updateprofile", status_code=201)
async def edit_user_profile():
    # record = user.dict()
    # email = record["email"]

    # filter = {"email": email}
    # update = {"$set": record}
    # with MongoClient() as client:
    #     collection = client[DB][USER_COLLECTION]
    #     collection.update_one(filter, update)

    # return {"message": "User profile updated successfully"}
    pass