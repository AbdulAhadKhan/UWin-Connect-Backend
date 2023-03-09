from fastapi import APIRouter

from models.posts import PostsModel
from utils.insertions import insert_post
from utils.retrieval import fetch_posts

post_router = APIRouter()


@post_router.post("/newspost", status_code=201)
async def news_post(post: PostsModel):
    print("debug", str(post))
    return {"insertion": insert_post(post)}


@post_router.get("/fetchposts/{name}")
async def retrieve_posts(name:str):
    posts = fetch_posts(name)
    posts = str(posts)
    return posts

