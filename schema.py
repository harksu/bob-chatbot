from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Access_Data(BaseModel):
    user_id: Optional[str] = None
    channel_id: Optional[str] = None
    access_time: Optional[datetime] = None
    access_id: Optional[str] = None

    class Config:
        orm_mode = True

class DevelopTechCreate(BaseModel):
    name: str
    description: Optional[str] = None
    habit: Optional[str] = None
    soju_count: Optional[float] = 0

class DevelopTech(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    habit: Optional[str] = None
    soju_count: Optional[float] = 0
    created_at: datetime

    class Config:
        orm_mode = True
