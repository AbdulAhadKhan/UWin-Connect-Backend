from pathlib import Path
from fastapi import APIRouter, Depends

from models.posts import PostsModel
from routes.user import get_user
from utils.utils import store_file
from utils.insertions import insert_post
from utils.retrieval import fetch_n_posts_by_user_le_time

post_router = APIRouter()


@post_router.post("/create-post", status_code=201)
async def new_post(post: PostsModel = Depends(PostsModel.as_form)):
    try:
        if not await get_user(post.email):
            return {"message": "User not found"}
        if post.image:
            post.image = await store_file(post.image)
        await insert_post(post)
        return {"message": "Post created successfully"}
    except Exception:
        Path(f".data/{post.image}").unlink(missing_ok=True)
        return {"message": "Post not created"}


@post_router.get("/get-posts/{email}", status_code=200)
async def get_posts(email: str, next_timestamp: int = 0, page_size: int = 10):
    try:
        posts, has_next, last_timestamp = await fetch_n_posts_by_user_le_time(
            email, next_timestamp, page_size)
        return {"posts": posts, "next": last_timestamp, "has_next": has_next}
    except Exception:
        return {"message": "Posts not retrieved"}
