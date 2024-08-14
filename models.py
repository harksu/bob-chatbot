from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from database import Base
from datetime import datetime

class Access_Table(Base):
    __tablename__ = 'access_table'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    channel_id = Column(String)
    access_time = Column(DateTime)
    access_id = Column(String)

class DevelopTech(Base):
    __tablename__ = "DevelopTech"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    habit = Column(Text, nullable=True)
    soju_count = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

