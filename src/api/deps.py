from fastapi import Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.user import User
from ..schemas.user import UserCreate

def get_current_user(db: Session = Depends(get_db), user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user