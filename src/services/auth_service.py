from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from src.models.user import User
from src.schemas.user import UserCreate, UserOut
from src.core.security import hash_password, verify_password
from src.core.database import get_db

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_create: UserCreate) -> UserOut:
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            (User.username == user_create.username) | 
            (User.email == user_create.email)
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create user without password field in the dict
        user_data = user_create.model_dump(exclude={'password'})
        user = User(**user_data)
        user.hashed_password = hash_password(user_create.password)
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return UserOut.model_validate(user)

    def authenticate_user(self, username: str, password: str) -> UserOut:
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return UserOut.model_validate(user)

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)