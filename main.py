from utils.retrieval import fetch_n_posts_by_user_le_time
from fastapi import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.posts import post_router
from routes.user import user_router
from routes.media import media_router

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)
app.include_router(media_router)


origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/echo")
async def echo(request: Request):
    """Echo the request body as JSON"""
    return await request.json()
