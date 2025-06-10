from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class WeatherSummary(BaseModel):
    temperature: float
    precipitation: float
    wind_speed: float
    condition: str

class WeatherAnalysis(BaseModel):
    suitability: str
    score: int
    reasons: List[str]
    weather_summary: WeatherSummary

class WeatherAlternative(BaseModel):
    date: str
    suitability: str
    score: int
    weather_summary: WeatherSummary

class WeatherResponse(BaseModel):
    location: str
    date: str
    current_weather: Dict[str, Any]
    analysis: Optional[WeatherAnalysis] = None
    alternatives: Optional[List[WeatherAlternative]] = None
