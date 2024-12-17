from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, func

from slugify import slugify

from app.backend.db_depends import get_db
from app.schemas import CreateEvent
from app.models import Event
import random


router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_events(db: Session = Depends(get_db)):
    row_count = db.query(func.count('*')).select_from(Event).scalar()
    random_index = random.randrange(0, row_count)
    random_row = db.query(Event).offset(random_index).limit(1).one()
    return random_row

@router.get("/{theater_name}")
async def get_event(theater_name: str, db: Session = Depends(get_db)):
    event = db.scalars(select(Event).where(Event.theater_name == theater_name)).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.get("/{date}")
async def get_event_by_date(date: str, db: Session = Depends(get_db)):
    event = db.scalars(select(Event).where(Event.date == date)).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

