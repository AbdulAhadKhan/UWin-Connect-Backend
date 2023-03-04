from pydantic import BaseModel

class NewSession(BaseModel):
    login_time: int
    machine_id: str
