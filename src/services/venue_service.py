from sqlalchemy.orm import Session
from src.models.venue import Venue
from src.schemas.venue import VenueCreate, VenueUpdate

class VenueService:
    def __init__(self, db: Session):
        self.db = db

    def create_venue(self, venue_create: VenueCreate) -> Venue:
        venue = Venue(**venue_create.model_dump())  # Changed from dict()
        self.db.add(venue)
        self.db.commit()
        self.db.refresh(venue)
        return venue

    def get_venue(self, venue_id: int) -> Venue:
        return self.db.query(Venue).filter(Venue.id == venue_id).first()

    def update_venue(self, venue_id: int, venue_update: VenueUpdate) -> Venue:
        venue = self.get_venue(venue_id)
        if venue:
            for key, value in venue_update.model_dump(exclude_unset=True).items():  # Changed from dict()
                setattr(venue, key, value)
            self.db.commit()
            self.db.refresh(venue)
        return venue

    def delete_venue(self, venue_id: int) -> bool:
        venue = self.get_venue(venue_id)
        if venue:
            self.db.delete(venue)
            self.db.commit()
            return True
        return False

    def get_all_venues(self) -> list[Venue]:
        return self.db.query(Venue).all()
