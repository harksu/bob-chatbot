from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Access_Data(BaseModel):
    user_id: Optional[str] = None
    channel_id: Optional[str] = None
    access_time: Optional[datetime] = None
    access_id: Optional[str] = None

    class Config:
        orm_mode = True

class User(BaseModel):
    user_id: str
    email: str

class UserEmail(BaseModel):
    email: str
