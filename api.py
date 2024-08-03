from fastapi import Depends, FastAPI
import logging
from sqlalchemy.orm import Session
from database import db
from schema import Access_Data

app = FastAPI()

@app.get("/")
async def root():
    logging.info("Hello World")
    return {"message": "Hello World"}

@app.post("/access")
async def access(access_item: Access_Data, access_db: Session = Depends(db.get_session)):
    pass
