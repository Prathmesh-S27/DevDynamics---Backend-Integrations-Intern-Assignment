from sqlalchemy import Column, Integer, String
from src.core.database import Base

class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    capacity = Column(Integer)
    description = Column(String)