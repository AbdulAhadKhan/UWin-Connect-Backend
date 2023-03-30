from fastapi import APIRouter, Form, Depends, Request, Body
from starlette.datastructures import FormData
from models.posts import PostsModel, FetchPostsModel, Comment
from utils.insertions import insert_post, insert_comment
from utils.retrieval import fetch_posts, getother_posts

post_router = APIRouter()


# @post_router.post("/newpost", status_code=201)
# async def new_post(post: PostsModel = Depends(PostsModel.as_form)):
#     print("debug", str(post))
#     return {"insertion": insert_post(post)}

@post_router.post("/newpost")
async def new_post(request: Request):
    formdata = await request.form()
    data = {}
    for key, value in formdata.items():
        if key != 'image':
            data[key] = value
    if formdata.get('image'):
        fileval = formdata['image']
        byteval = await fileval.read()
        data['image'] = byteval
    post = PostsModel.parse_obj(data)
    # print("debug", str(post))
    return {"insertion": insert_post(post)}


@post_router.post("/newcomment/{id_val}", status_code=201)
async def new_comment(comment: Comment, id_val: str):
    print("debug", str(comment))
    return {"inserted comment": insert_comment(id_val, comment)}


@post_router.get("/fetchposts/{name}")
async def retrieve_posts(name: str):
    posts = await fetch_posts(name)
    posts = str(posts)
    return posts


@post_router.post("/getotherposts/")
async def retrieve_other_posts(fetchpostsmodel: FetchPostsModel):
    posts = await getother_posts(fetchpostsmodel.userid, fetchpostsmodel.last_time)
    posts = str(posts)
    return posts


