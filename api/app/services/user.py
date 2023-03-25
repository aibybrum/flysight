import bcrypt
from uuid import UUID, uuid4
from api.app.schemas.user import UserCreate, UserUpdate
from api.app.models.user import User
from api.app.services.main import PostgresService


class UserCRUD(PostgresService):
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


class UserService(UserCRUD):
    def check_username(self, username: str) -> bool:
        db_user = self.db.query(User).filter(User.username == username).first()
        if db_user:
            return True
        else:
            return False





