import hashlib
import json
import requests
from sqlalchemy.orm import Session
import models
import schema
from config import conf

def write_access_data_in_db(access_id: str, access_item: schema.Access_Data, db: Session):
    pass
