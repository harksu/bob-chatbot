from fastapi import Depends, FastAPI, HTTPException
import logging
from sqlalchemy.orm import Session
from database import db
from schema import Access_Data,User
import crud
from typing import List  

app = FastAPI()

@app.get("/")
async def root():
    logging.info("Hello World")
    return {"message": "Hello World"}

@app.post("/access")
async def access(access_item: Access_Data, access_db: Session = Depends(db.get_session)):
    pass


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(db.get_session)):
    try:
        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except Exception as e:
        logging.error(f"Error reading user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_session)):
    try:
        users = crud.get_users(db, skip=skip, limit=limit)
        return users
    except Exception as e:
        logging.error(f"Error reading users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")