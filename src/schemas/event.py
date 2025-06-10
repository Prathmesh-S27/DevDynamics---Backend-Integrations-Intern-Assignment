from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .weather import WeatherAnalysis

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: str
    event_type: str = "general"  # outdoor, indoor, sports, festival, etc.

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    event_type: Optional[str] = None

class Event(EventBase):
    id: int
    weather_analysis: Optional[WeatherAnalysis] = None

    class Config:
        from_attributes = True  # Changed from orm_mode

class EventList(BaseModel):
    events: List[Event]

class EventWeatherCheck(BaseModel):
    event_id: int
    weather_analysis: WeatherAnalysis