from pydantic import BaseModel

class CreateEvent(BaseModel):
    title: str
    description: str
    date: str
    time: str


