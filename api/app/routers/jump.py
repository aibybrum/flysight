from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from uuid import UUID

from app.services.jump.jump_service import JumpService
from app.schemas.jump import Jump, JumpCreate
from app.utils.service_result import handle_result
from app.dependencies import get_jump_service

router = APIRouter(
    prefix="/jumps",
    tags=["Jump"],
    responses={404: {"description": "Not found"}},
)


@router.get("/user/{user_id}", response_model=List[Jump])
async def get_jumps_by_user(user_id: UUID, jump_service: JumpService = Depends(get_jump_service)):
    result = jump_service.get_jumps_by_user(user_id)
    return handle_result(result)


@router.post("", response_model=JumpCreate)
async def create_jump(user_id: UUID, csv_file: UploadFile = File(...), jump_service: JumpService = Depends(get_jump_service)):
    result = jump_service.create_jump(user_id, csv_file)
    return handle_result(result)


@router.delete("/{jump_id}")
async def delete_jump(jump_id: UUID, jump_service: JumpService = Depends(get_jump_service)):
    result = jump_service.delete_jump(jump_id)
    return handle_result(result)


@router.delete("/user/{user_id}")
async def delete_jumps_by_user(user_id: UUID, jump_service: JumpService = Depends(get_jump_service)):
    result = jump_service.delete_jumps_by_user(user_id)
    return handle_result(result)