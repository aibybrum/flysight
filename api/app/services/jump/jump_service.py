from uuid import UUID, uuid4

from fastapi import UploadFile
from app.services.jump.jump_crud import JumpCRUD
from app.schemas.jump import Jump, JumpCreate
from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult


class JumpService():
    def __init__(self, user_service):
        self.user_service = user_service

    def get_jumps_by_user(self, user_id: UUID) -> ServiceResult:
        user_result = self.user_service.get_user(user_id)
        if not user_result.success:
            return user_result

        db_jumps = JumpCRUD().get_jumps_by_user(user_id)
        return ServiceResult(db_jumps)

    def create_jump(self, user_id: UUID, file: UploadFile) -> ServiceResult:
        user_result = self.user_service.get_user(user_id)
        if not user_result.success:
            return user_result

        db_jump = JumpCRUD().create_jump(user_id, file)
        if not db_jump:
            return ServiceResult(AppException.CreateJump())
        return ServiceResult(db_jump)

    def delete_jump(self, jump_id: UUID) -> ServiceResult:
        db_jump = JumpCRUD().get_jump(jump_id)
        if db_jump is None:
            return ServiceResult(AppException.JumpNotFound())
        try:
            JumpCRUD().delete_jump(jump_id)
        except (Exception ,):
            return ServiceResult(AppException.JumpNotModified())
        return ServiceResult({"message": "Jump deleted successfully"})

    def delete_jumps_by_user(self, user_id: UUID) -> ServiceResult:
        user_result = self.user_service.get_user(user_id)
        if not user_result.success:
            return user_result

        jumps_to_delete = JumpCRUD().get_jumps_by_user(user_id)
        if not jumps_to_delete:
            return ServiceResult({"message": f"User {user_id} has no jumps logged"})
        
        for jump in jumps_to_delete:
            try:
                JumpCRUD().delete_jump(jump.id)
            except (Exception ,):
                return ServiceResult(AppException.JumpNotModified())
        return ServiceResult({"message": f"All jumps for user {user_id} deleted succesfully"})
