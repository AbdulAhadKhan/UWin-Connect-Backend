from fastapi import APIRouter

from models.posts import PostsModel, FetchPostsModel
from utils.insertions import insert_post
from utils.retrieval import fetch_posts, getother_posts

post_router = APIRouter()


@post_router.post("/newspost", status_code=201)
async def news_post(post: PostsModel):
    print("debug", str(post))
    return {"insertion": insert_post(post)}


@post_router.get("/fetchposts/{name}")
async def retrieve_posts(name: str):
    posts = fetch_posts(name)
    posts = str(posts)
    return posts


@post_router.post("/getotherposts/")
async def retrieve_other_posts(fetchpostsmodel:FetchPostsModel):
    posts = await getother_posts(fetchpostsmodel.userid, fetchpostsmodel.last_time)
    posts = str(posts)
    return posts
