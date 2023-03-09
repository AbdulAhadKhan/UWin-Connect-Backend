from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import Optional
from typing import List, Tuple



class PostsModel(BaseModel):
    userid: str
    title: str
    description: str
    timestamp: datetime
    # image: UploadFile = File(...)
    comments: Optional[List[Tuple[str,datetime]]]