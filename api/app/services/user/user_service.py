from uuid import UUID, uuid4

from app.models.user import User
from sqlalchemy.orm import Session
from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult
from app.services.user.user_crud import UserCRUD
from app.services.postgres_service import AppService
from app.schemas.user import UserCreate, UserUpdate


class UserService(AppService):
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
        user_result = self.get_user(user_id)
        if not user_result.success:
            return user_result
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
