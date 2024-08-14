from sqlalchemy import Column, DateTime, Integer, String 
from database import Base

class Access_Table(Base):
    __tablename__ = 'access_table'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    channel_id = Column(String)
    access_time = Column(DateTime)
    access_id = Column(String)

