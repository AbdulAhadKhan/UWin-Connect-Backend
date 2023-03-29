from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import Optional
from typing import List
from typing import Union
from fastapi import UploadFile
from utils.helpers import form


class Comment(BaseModel):
    author: str
    text: str


@form
class PostsModel(BaseModel):
    email: str
    description: str
    timestamp: int
    image: Union[UploadFile, None] = None


class FetchPostsModel(BaseModel):
    userid: str
    last_time: str
