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
    user_name: str
    user_email: str
    access_time: datetime
    access_ip: str
    id : int

    class Config:
        orm_mode = True

class UserEmail(BaseModel):
    user_email: str
    access_time: datetime
