from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True  # Changed from orm_mode

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserRead):
    hashed_password: str