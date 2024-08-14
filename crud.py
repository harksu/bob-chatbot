import hashlib
import json
import requests
from sqlalchemy.orm import Session
import models
import schema
from config import conf
import logging
from datetime import datetime



def create_developtech(db: Session, developtech: schema.DevelopTechCreate):
    db_developtech = models.DevelopTech(
        name=developtech.name,
        description=developtech.description,
        habit=developtech.habit,
        soju_count=developtech.soju_count
    )
    db.add(db_developtech)
    db.commit()
    db.refresh(db_developtech)
    return db_developtech

def get_developtech_by_email(db: Session, name: str):
    return db.query(models.DevelopTech).filter(models.DevelopTech.name == name).first()