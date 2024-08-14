from fastapi import FastAPI, Depends
import crud
from vt import virustotal
from bot import SLACK_CLIENT, process  

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
