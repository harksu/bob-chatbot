import hashlib
import json
import requests
from sqlalchemy.orm import Session
import models
import schema
from config import conf
import logging
from datetime import datetime


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

def get_user_by_email(db: Session, user_email: str):
    try:
        return db.query(models.User).filter(models.User.user_email == user_email).all()
    except Exception as e:
        logging.error(f"Error getting user by email: {e}")
        raise

def update_user_access(db: Session, user_email: str, access_time: datetime, access_ip: str):
    try:
        user = db.query(models.User).filter(models.User.user_email == user_email).first()
        if user:
            user.access_time = access_time
            user.access_ip = access_ip
            db.commit()
            db.refresh(user)
            return user
        else:
            return None
    except Exception as e:
        logging.error(f"Error updating user access: {e}")
        db.rollback()
        raise