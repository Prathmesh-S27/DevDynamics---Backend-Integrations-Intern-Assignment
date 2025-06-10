from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserRead
from src.services.user_service import UserService
from src.core.database import get_db

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    created_user = user_service.create_user(user)
    return created_user

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserRead])
async def list_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    users = user_service.get_all_users()
    return users