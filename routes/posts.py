from pathlib import Path
from fastapi import APIRouter, Form, Depends

from models.posts import PostsModel, FetchPostsModel
from routes.user import get_user
from utils.insertions import insert_post
from utils.utils import store_file
from utils.retrieval import fetch_posts, getother_posts

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


@post_router.get("/fetchposts/{name}")
async def retrieve_posts(name: str):
    posts = fetch_posts(name)
    posts = str(posts)
    return posts


@post_router.post("/getotherposts/")
async def retrieve_other_posts(fetchpostsmodel: FetchPostsModel):
    posts = await getother_posts(fetchpostsmodel.userid, fetchpostsmodel.last_time)
    posts = str(posts)
    return posts
