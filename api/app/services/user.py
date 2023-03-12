from api.app.schemas.user import UserCreate
from api.app.utils.app_exceptions import AppException

from api.app.services.main import AppService, AppCRUD
from api.app.models.user import User
from api.app.utils.service_result import ServiceResult
from fastapi.encoders import jsonable_encoder


class UserService(AppService):
    def get_users(self) -> ServiceResult:
        user = UserCRUD(self.db).get_users()
        return ServiceResult(user)

    def get_user(self, user_id: int) -> ServiceResult:
        user = UserCRUD(self.db).get_user(user_id)
        if not user:
            return ServiceResult(AppException.GetUser({"user_id": user_id}))
        return ServiceResult(user)

    def create_user(self, user: UserCreate) -> ServiceResult:
        user = UserCRUD(self.db).create_user(user)
        if not user:
            return ServiceResult(AppException.CreateUser())
        return ServiceResult(user)

    def delete_user(self, user_id: int) -> ServiceResult:
        user = UserCRUD(self.db).get_user(user_id)
        if not user:
            return ServiceResult(AppException.GetUser({"user_id": user_id}))
        try:
            UserCRUD(self.db).delete_user(user_id)
        except (Exception,):
            return ServiceResult(AppException.DeleteUser())
        return ServiceResult(user)

    def update_user(self, user_id: int, user: User) -> ServiceResult:
        if user_id != user.id:
            return ServiceResult(AppException.UpdateUser.bad_request())
        user = UserCRUD(self.db).update_user(user_id)
        if not user:
            return ServiceResult(AppException.UpdateUser())
        return ServiceResult(user)


class UserCRUD(AppCRUD):
    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            return user
        return None

    def create_user(self, user: UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = User(username=user.username, hashed_password=fake_hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
            return user
        return None

    def update_user(self, user_id: int, user: User):
        old_user = self.db.query(User).filter(User.id == user_id).first()
        if old_user:
            user =



