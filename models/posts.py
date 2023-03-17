from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import Optional
from typing import List


class Comment(BaseModel):
    author: str
    text: str

class PostsModel(BaseModel):
    userid: str
    title: str
    description: str
    timestamp: datetime
    # image: UploadFile = File(...)
    comment: Optional[List[Comment]] = None


class FetchPostsModel(BaseModel):
    userid: str
    last_time: str



