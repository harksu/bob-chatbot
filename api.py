from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
from sqlalchemy.orm import Session
from database import db
from schema import Access_Data, User, UserEmail
import crud
from typing import List
from datetime import datetime

app = FastAPI()

# Static and template configuration
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/access")
async def access(access_item: Access_Data, access_db: Session = Depends(db.get_session)):
    access_id = hashlib.sha256(f"{access_item.user_id}{access_item.channel_id}{access_item.access_time}".encode()).hexdigest()
    try:
        access_data = crud.write_access_data_in_db(access_id, access_item, access_db)
        return {"message": "Access data recorded", "access_id": access_id}
    except Exception as e:
        logging.error(f"Error recording access data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/users/", response_model=User)
async def create_user(user: User, db: Session = Depends(db.get_session)):
    try:
        return crud.create_user(db=db, user=user)
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

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

@app.get("/users/email/{user_email}", response_model=List[User])
async def read_users_by_email(user_email: str, db: Session = Depends(db.get_session)):
    try:
        users = crud.get_user_by_email(db, user_email=user_email)
        if not users:
            raise HTTPException(status_code=404, detail="User not found")
        return users
    except Exception as e:
        logging.error(f"Error reading user by email: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/check_email/")
async def check_email(user_email: UserEmail, request: Request, db: Session = Depends(db.get_session)):
    try:
        current_time = user_email.access_time
        access_ip = request.client.host  # 클라이언트의 IP 주소를 가져옵니다.
        
        user = crud.get_user_by_email(db=db, user_email=user_email.user_email)
        if user:
            updated_user = crud.update_user_access(db, user_email=user_email.user_email, access_time=current_time, access_ip=access_ip)
            return {"message": "welcome", "user_email": user_email.user_email}
        else:
            return {"message": "reject"}
    except Exception as e:
        logging.error(f"Error checking user email: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
