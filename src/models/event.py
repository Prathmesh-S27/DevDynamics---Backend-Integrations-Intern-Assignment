from sqlalchemy import Column, Integer, String, DateTime, JSON
from src.core.database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # Changed from 'name' to 'title'
    description = Column(String, nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    event_type = Column(String, default="general")  # New field
    weather_data = Column(JSON, nullable=True)  # Store weather analysis
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)