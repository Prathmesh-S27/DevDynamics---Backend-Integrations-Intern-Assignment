from sqlalchemy.orm import Session
from src.models.event import Event
from src.schemas.event import EventCreate, EventUpdate
from src.services.weather_service import WeatherService
from datetime import datetime

class EventService:
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService()

    def create_event(self, event: EventCreate) -> Event:
        db_event = Event(**event.model_dump())  # Changed from dict()
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def get_event(self, event_id: int) -> Event:
        return self.db.query(Event).filter(Event.id == event_id).first()

    def update_event(self, event_id: int, event: EventUpdate) -> Event:
        db_event = self.get_event(event_id)
        if db_event:
            for key, value in event.model_dump(exclude_unset=True).items():  # Changed from dict()
                setattr(db_event, key, value)
            self.db.commit()
            self.db.refresh(db_event)
        return db_event

    def delete_event(self, event_id: int) -> bool:
        db_event = self.get_event(event_id)
        if db_event:
            self.db.delete(db_event)
            self.db.commit()
            return True
        return False

    def get_all_events(self) -> list[Event]:
        return self.db.query(Event).all()

    async def analyze_event_weather(self, event_id: int) -> dict:
        """Analyze weather for a specific event"""
        event = self.get_event(event_id)
        if not event:
            return {"error": "Event not found"}
        
        # Get weather for event date
        weather_data = await self.weather_service.get_current_weather(event.location)
        analysis = self.weather_service.analyze_weather_suitability(weather_data, event.event_type)
        
        # Store weather analysis in event
        event.weather_data = {
            "analysis": analysis,
            "fetched_at": datetime.utcnow().isoformat()
        }
        self.db.commit()
        
        return analysis

    async def get_event_alternatives(self, event_id: int) -> list:
        """Get alternative dates for an event with better weather"""
        event = self.get_event(event_id)
        if not event:
            return []
        
        return await self.weather_service.get_alternative_dates(
            event.location, event.start_time, event.event_type
        )