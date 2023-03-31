import sys

from typing import Union
from fastapi import Response, status, APIRouter, Depends, HTTPException, UploadFile

from utils.verifications import email_exists, verify_password, check_if_friends
from utils.insertions import insert_user, insert_session
from utils.updates import update_user, push_friend, pop_friend
from utils.retrieval import fetch_user, get_user_minimal_info
from utils.utils import store_file
from utils.search import search_users
from models.user import Registration, Login, UserUpdate, UserFullResponse

user_router = APIRouter()


@user_router.post("/signup", status_code=201, responses={201: {"description": "User created successfully"},
                                                         409: {"description": "Email already exists"}})
async def register(user_info: Registration, response: Response):
    """Register a new user"""

    # Check if email already exists
    if email_exists(user_info.email):
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Email already exists"}

    # Insert user into database
    await insert_user(user_info)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "User created successfully"}


@user_router.post("/login", status_code=200, responses={200: {"description": "Login successful"},
                                                        401: {"description": "Invalid credentials"}})
async def login(user: Login, response: Response):
    if email_exists(user.email) and verify_password(user.email, user.password):
        session_id = await insert_session(user.email, user.meta)
        return {"message": "Login successful", "session_id": session_id}
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"message": "Invalid credentials"}


@user_router.put("/update-user/{email}", status_code=200, responses={200: {"description": "User updated successfully"}})
async def update(response: Response, data: UserUpdate, email: str):
    try:
        await update_user(email, data)
        return {"message": "User updated successfully"}
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(sys.exc_info())
        return {"message": "User not updated"}


@user_router.get("/get-user/{email}", response_model=Union[UserFullResponse, None], status_code=200,
                 responses={200: {"description": "User retrieved successfully"},
                            404: {"description": "User not found"}})
async def get_user(email: str):
    user = await fetch_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.put("/upload-profile-picture/{email}", status_code=200, responses={200: {"description": "Profile picture set successfully"}})
async def set_profile_picture(response: Response, image: UploadFile, email: str):
    try:
        user = await fetch_user(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user['image'] = await store_file(image)
        await update_user(email, user)
        return {"message": "Profile picture set successfully",
                "image": user['image']}
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Profile picture not set"}


@user_router.get("/query-users/{query}", status_code=200, responses={200: {"description": "Users retrieved successfully"}})
async def query_users(query: str):
    users = await search_users(query)
    return users


@user_router.get("/get-user-minimal-info/{email}", status_code=200, responses={200: {"description": "User retrieved successfully"}})
async def get_minimal_user(email: str):
    user = await get_user_minimal_info(email)
    return user


@user_router.get("/friendship-status",
                 status_code=200, responses={200: {"description": "Friendship status retrieved successfully"}})
async def are_friends(email: str, friends_email: str):
    return {"are_friends": check_if_friends(email, friends_email)}


@user_router.get("/add-friend", status_code=200, responses={200: {"description": "Friend added successfully"}})
async def add_friend(email: str, friends_email: str):
    try:
        push_friend(email, friends_email)
        return {"message": "Friend added successfully"}
    except Exception:
        print(sys.exc_info())
        return {"message": "Friend not added"}


@user_router.get("/remove-friend", status_code=200, responses={200: {"description": "Friend removed successfully"}})
async def remove_friend(email: str, friends_email: str):
    try:
        pop_friend(email, friends_email)
        return {"message": "Friend removed successfully"}
    except Exception:
        print(sys.exc_info())
        return {"message": "Friend not removed"}
