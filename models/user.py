from pydantic import BaseModel

class User(BaseModel):
    userid: str
    email: str
    password: str