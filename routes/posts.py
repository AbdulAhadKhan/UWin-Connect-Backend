import sys

from pathlib import Path
from fastapi import APIRouter, Depends, Request

from models.posts import PostsModel, CommentModel
from routes.user import get_user
from utils.utils import store_file
from utils.insertions import insert_post
from utils.retrieval import fetch_n_posts_by_user_le_time, fetch_n_posts_by_friends
from utils.updates import push_like, pop_like, push_comment

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
async def get_posts(email: str, next_timestamp: int, page_size: int = 10):
    try:
        posts, last_timestamp = await fetch_n_posts_by_user_le_time(
            email, next_timestamp, page_size)
        return {"posts": posts, "next": {"page": last_timestamp} if last_timestamp else None}
    except Exception:
        print(sys.exc_info())
        return {"message": "Posts not retrieved"}


@post_router.get("/get-friends-posts/{email}", status_code=200)
async def get_friends_posts(email: str, next_timestamp: int, page_size: int = 10):
    try:
        posts, last_timestamp = await fetch_n_posts_by_friends(
            email, next_timestamp, page_size)
        return {"posts": posts, "next": {"page": last_timestamp} if last_timestamp else None}
    except Exception:
        print(sys.exc_info())
        return {"message": "Posts not retrieved"}


@post_router.put("/like-post/{post_id}", status_code=200)
async def like_post(email: str, post_id: str):
    try:
        push_like(email, post_id)
        return {"message": "Post liked successfully"}
    except Exception:
        print(sys.exc_info())
        return {"message": "Post not liked"}


@post_router.put("/unlike-post/{post_id}", status_code=200)
async def unlike_post(email: str, post_id: str):
    try:
        pop_like(email, post_id)
        return {"message": "Post unliked successfully"}
    except Exception:
        print(sys.exc_info())
        return {"message": "Post not unliked"}


@post_router.post("/comment-post/{post_id}", status_code=200)
async def comment_post(post_id: str, comment: CommentModel = Depends(CommentModel.as_form)):
    try:
        push_comment(comment.email, post_id,
                     comment.comment, comment.timestamp)
        return {"message": "Post commented successfully"}
    except Exception:
        print(sys.exc_info())
        return {"message": "Post not commented"}
