from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from src.schemas.event import EventCreate, EventUpdate, Event
from src.services.event_service import EventService
from src.services.weather_service import WeatherService
from src.core.database import get_db

router = APIRouter()

@router.post("/", response_model=Event, status_code=201)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    event_service = EventService(db)
    return event_service.create_event(event)

@router.get("/", response_model=List[Event])
async def get_events(db: Session = Depends(get_db)):
    event_service = EventService(db)
    return event_service.get_all_events()

@router.get("/{event_id}", response_model=Event)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    event_service = EventService(db)
    event = event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=Event)
async def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    event_service = EventService(db)
    updated_event = event_service.update_event(event_id, event)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event

@router.delete("/{event_id}", status_code=204)
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    event_service = EventService(db)
    success = event_service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")

@router.post("/{event_id}/weather-check", response_model=dict)
async def check_event_weather(event_id: int, db: Session = Depends(get_db)):
    """Analyze weather for existing event"""
    event_service = EventService(db)
    analysis = await event_service.analyze_event_weather(event_id)
    if "error" in analysis:
        raise HTTPException(status_code=404, detail=analysis["error"])
    return {"event_id": event_id, "weather_analysis": analysis}

@router.get("/{event_id}/alternatives", response_model=List[dict])
async def get_event_alternatives(event_id: int, db: Session = Depends(get_db)):
    """Get better weather dates for event"""
    event_service = EventService(db)
    alternatives = await event_service.get_event_alternatives(event_id)
    return alternatives

@router.get("/{event_id}/suitability", response_model=dict)
async def get_event_suitability(event_id: int, db: Session = Depends(get_db)):
    """Get weather suitability score for event"""
    event_service = EventService(db)
    event = event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event.weather_data and "analysis" in event.weather_data:
        return event.weather_data["analysis"]
    
    # If no cached weather data, fetch fresh analysis
    analysis = await event_service.analyze_event_weather(event_id)
    return analysis

@router.get("/{event_id}/weather-analysis", response_model=dict)
async def get_enhanced_weather_analysis(event_id: int, db: Session = Depends(get_db)):
    """Get comprehensive weather analysis for event"""
    event_service = EventService(db)
    event = event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    weather_service = WeatherService()
    
    # Get all enhanced weather data
    current_weather = await weather_service.get_current_weather(event.location)
    hourly_forecast = await weather_service.get_weather_for_event_duration(
        event.location, event.start_time, event.end_time
    )
    trends = await weather_service.analyze_weather_trends(event.location, event.start_time)
    nearby_comparison = await weather_service.compare_nearby_locations(event.location)
    
    return {
        "event_id": event_id,
        "current_weather": current_weather,
        "hourly_forecast": hourly_forecast,
        "weather_trends": trends,
        "nearby_locations": nearby_comparison
    }

@router.get("/{event_id}/recommendations", response_model=dict)
async def get_rescheduling_recommendations(event_id: int, db: Session = Depends(get_db)):
    """Get smart rescheduling recommendations"""
    from src.services.notification_service import NotificationService
    notification_service = NotificationService(db)
    return await notification_service.get_rescheduling_recommendations(event_id)