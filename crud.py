import hashlib
import json
import requests
from sqlalchemy.orm import Session
import models
import schema
from config import conf
import logging


def write_access_data_in_db(access_id: str, access_item: schema.Access_Data, db: Session):
    pass

def get_user(db: Session, user_id: int):
    try:
        return db.query(models.User).filter(models.User.id == user_id).first()
    except Exception as e:
        logging.error(f"Error getting user: {e}")
        raise

def get_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.User).offset(skip).limit(limit).all()
    except Exception as e:
        logging.error(f"Error getting users: {e}")
        raise