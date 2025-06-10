from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate) -> User:
        user = User(**user_create.model_dump())  # Changed from dict()
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.get_user(user_id)
        if user:
            for key, value in user_update.model_dump(exclude_unset=True).items():  # Changed from dict()
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()