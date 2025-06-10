from typing import Optional
from pydantic import BaseModel

class VenueBase(BaseModel):
    name: str
    location: str
    capacity: Optional[int] = None

class VenueCreate(VenueBase):
    pass

class VenueUpdate(VenueBase):
    pass

class VenueRead(VenueBase):  # Added missing schema
    id: int

    class Config:
        from_attributes = True  # Changed from orm_mode

class Venue(VenueBase):
    id: int

    class Config:
        from_attributes = True  # Changed from orm_mode