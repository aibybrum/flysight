import bcrypt
from uuid import UUID, uuid4

from app.models.user import User
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.services.postgres_service import AppCRUD

class UserCRUD(AppCRUD):
    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user(self, user_id: UUID):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: UserCreate):
        password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        db_user = User(id=uuid4(), username=user.username, hashed_password=password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: UUID):
        user = self.db.query(User).filter(User.id == user_id).first()
        self.db.delete(user)
        self.db.commit()

    def update_user(self, user_id: UUID, user: UserUpdate):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        db_user.username = user.username
        db_user.password = user.password
        self.db.commit()
        self.db.refresh(db_user)
        return db_user