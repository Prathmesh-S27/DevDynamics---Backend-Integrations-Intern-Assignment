from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.services.auth_service import AuthService, get_auth_service
from src.core.database import get_db

router = APIRouter()

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

@router.post("/login")
async def login(user: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    try:
        user_out = auth_service.authenticate_user(user.username, user.password)
        return {"access_token": "dummy_token", "user": user_out}
    except HTTPException as e:
        raise e

@router.post("/register")
async def register(user: UserRegister, auth_service: AuthService = Depends(get_auth_service)):
    from src.schemas.user import UserCreate
    user_create = UserCreate(**user.model_dump())  # Changed from dict()
    user_out = auth_service.register_user(user_create)
    return {"message": "User created successfully", "user": user_out}