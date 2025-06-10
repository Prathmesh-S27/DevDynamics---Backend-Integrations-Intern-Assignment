from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from src.schemas.venue import VenueCreate, VenueRead, VenueUpdate
from src.services.venue_service import VenueService
from src.core.database import get_db

router = APIRouter()

@router.post("/", response_model=VenueRead)
async def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    venue_service = VenueService(db)
    return venue_service.create_venue(venue)

@router.get("/", response_model=List[VenueRead])
async def get_venues(db: Session = Depends(get_db)):
    venue_service = VenueService(db)
    return venue_service.get_all_venues()

@router.get("/{venue_id}", response_model=VenueRead)
async def get_venue(venue_id: int, db: Session = Depends(get_db)):
    venue_service = VenueService(db)
    venue = venue_service.get_venue(venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue

@router.put("/{venue_id}", response_model=VenueRead)
async def update_venue(venue_id: int, venue: VenueUpdate, db: Session = Depends(get_db)):
    venue_service = VenueService(db)
    updated_venue = venue_service.update_venue(venue_id, venue)
    if not updated_venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return updated_venue

@router.delete("/{venue_id}", response_model=dict)
async def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    venue_service = VenueService(db)
    success = venue_service.delete_venue(venue_id)
    if not success:
        raise HTTPException(status_code=404, detail="Venue not found")
    return {"message": "Venue deleted successfully"}