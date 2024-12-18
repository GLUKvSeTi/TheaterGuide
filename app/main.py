from fastapi import FastAPI
from app.scrappers.scrapper import parse_tt_afisha
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, func
from urllib3 import request
from fastapi.responses import HTMLResponse

from app.backend.db_depends import get_db
from fastapi.templating import Jinja2Templates
from app.schemas import CreateEvent
from app.models import Event
import random

from app.scrappers.scrapper import parse_tt_afisha
import time
import threading
import schedule
'''
parse_tt_afisha()
parse_tuz_afisha()
'''

app = FastAPI()
def start_scheduler():
    schedule.every(10).minutes.do(parse_tt_afisha)
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.on_event("startup")
def startup_event():
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

templates = Jinja2Templates(directory="app/templates")
@app.get('/')
async def get_events(request: Request, db: Session = Depends(get_db)):
    row_count = db.query(func.count('*')).select_from(Event).scalar()
    random_index = random.randrange(0, row_count)
    random_row = db.query(Event).offset(random_index).limit(1).one()
    return templates.TemplateResponse("performance.html", {"request": request, "performance": random_row})



