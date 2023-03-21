from pathlib import Path
from fastapi import Response, status, APIRouter, Depends

from utils.verifications import email_exists, verify_password
from utils.insertions import insert_user, insert_session
from utils.updates import update_user
from utils.retrieval import fetch_user
from utils.utils import store_file
from models.user import Registration, Login, UserFull, UserFullResponse

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
    insert_user(user_info)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "User created successfully"}

@user_router.post("/login", status_code=200, responses={200: {"description": "Login successful"},
                                                        401: {"description": "Invalid credentials"}})
async def login(user: Login, response: Response):
    if email_exists(user.email) and verify_password(user.email, user.password):
        session_id = insert_session(user.email, user.meta)
        return {"message": "Login successful", "session_id": session_id}
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"message": "Invalid credentials"}

@user_router.put("/update-user", status_code=200, responses={200: {"description": "User updated successfully"}})
async def update(response: Response, user: UserFull = Depends(UserFull.as_form)):
    try:
        user.image = await store_file(user.image)
        await update_user(user)
        return {"message": "User updated successfully"}
    except Exception:
        Path(f".data/{user.image}").unlink(missing_ok=True)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "User not updated"}

@user_router.get("/get-user/{email}", response_model=UserFullResponse)
async def get_user(email: str):
    return await fetch_user(email)
