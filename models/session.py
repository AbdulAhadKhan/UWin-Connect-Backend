from pydantic import BaseModel

class NewSession(BaseModel):
    login_time: int
    machine_id: str

class Session(BaseModel):
    session_id: str
    user_id: str
    login_time: int
    machine_id: str
