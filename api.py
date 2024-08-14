from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import logging
import crud
from sqlalchemy.orm import Session
from database import db
from vt import virustotal
from bot import SLACK_CLIENT, process  
from models import DevelopTech
import schema
from typing import List  # List를 가져옵니다.


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/vt/{query_item}/{query_type}")
async def vt_query(query_item: str, query_type: str):
    return virustotal(query_item, query_type)

@app.on_event("startup")
async def startup_event():
    SLACK_CLIENT.socket_mode_request_listeners.append(process)
    SLACK_CLIENT.connect()

@app.post("/developtechs/", response_model=schema.DevelopTech)
def create_developtech(developtech: schema.DevelopTechCreate, db: Session = Depends(db.get_session)):
    """
    DevelopTech 테이블에 새로운 레코드를 생성하는 API 엔드포인트.
    """
    return crud.create_developtech(db=db, developtech=developtech)


@app.get("/developtechs/{name}", response_model=schema.DevelopTech)
def read_developtech(name: str, db: Session = Depends(db.get_session)):
    """
    DevelopTech 테이블에서 특정 이메일을 가진 데이터를 조회하는 API 엔드포인트.
    """
    developtech = crud.get_developtech_by_email(db, name=name)
    if developtech is None:
        raise HTTPException(status_code=404, detail="DevelopTech not found")
    return developtech
