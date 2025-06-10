from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schemas.weather import WeatherResponse, WeatherAnalysis
from src.services.weather_service import WeatherService
from src.core.database import get_db
from datetime import datetime

router = APIRouter()

@router.get("/{location}/{date}", response_model=dict)
async def get_weather_for_location_and_date(location: str, date: str):
    """Get weather data for specific location and date"""
    weather_service = WeatherService()
    
    try:
        # Parse date
        target_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")
    
    # Get current weather (for demo, in real app you'd need historical/forecast data)
    weather_data = await weather_service.get_current_weather(location)
    
    if "error" in weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found for location")
    
    return {
        "location": location,
        "date": date,
        "weather_data": weather_data
    }
