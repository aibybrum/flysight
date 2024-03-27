import bcrypt
from uuid import UUID, uuid4

from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.services.main import PostgresService, PostgresCRUD
from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult


class UserService(PostgresService):
    def get_users(self) -> ServiceResult:
        db_users = UserCRUD(self.db).get_users()
        return ServiceResult(db_users)

    def get_user(self, user_id: UUID) -> ServiceResult:
        db_user = UserCRUD(self.db).get_user(user_id)
        if db_user is None:
            return ServiceResult(AppException.UserNotFound())
        return ServiceResult(db_user)

    def create_user(self, user: UserCreate) -> ServiceResult:
        if self.check_username(user.username):
            return ServiceResult(AppException.UsernameAlreadyExists())
        db_user = UserCRUD(self.db).create_user(user)
        if not db_user:
            return ServiceResult(AppException.CreateUser())
        return ServiceResult(db_user)

    def delete_user(self, user_id: UUID) -> ServiceResult:
        db_user = UserCRUD(self.db).get_user(user_id)
        if db_user is None:
            return ServiceResult(AppException.UserNotFound())
        try:
            UserCRUD(self.db).delete_user(user_id)
        except (Exception,):
            return ServiceResult(AppException.UserNotModified())
        return ServiceResult({"message": "User deleted successfully"})

    def update_user(self, user_id: UUID, user: UserUpdate) -> ServiceResult:
        db_user = UserCRUD(self.db).get_user(user_id)
        if db_user is None:
            return ServiceResult(AppException.UserNotFound())
        try:
            UserCRUD(self.db).update_user(user_id, user)
        except (Exception,):
            return ServiceResult(AppException.UserNotModified())
        return ServiceResult(db_user)

    def check_username(self, username: str) -> bool:
        db_user = self.db.query(User).filter(User.username == username).first()
        if db_user:
            return True
        else:
            return False


class UserCRUD(PostgresCRUD):
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
