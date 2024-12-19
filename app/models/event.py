from app.backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable
from app.backend.db import engine

class Event(Base):
    __tablename__ = 'events'
    __table_args__ = {'extend_existing': True}
    theater_name = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    title= Column(String)
    date = Column(String)
    time = Column(String)
    description = Column(String)

Base.metadata.create_all(bind=engine)