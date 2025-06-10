from fastapi import APIRouter
from .endpoints import events, venues, weather, notifications

api_router = APIRouter()

api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(venues.router, prefix="/venues", tags=["venues"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])