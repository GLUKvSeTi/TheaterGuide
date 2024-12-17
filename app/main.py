from fastapi import FastAPI
from app.routers import events
from app.scrappers.scrapper1 import parse_tt_afisha
from app.scrappers.scrapper2 import parse_tuz_afisha

parse_tt_afisha()
parse_tuz_afisha()
app = FastAPI()

app.include_router(events.router)