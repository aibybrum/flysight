from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import UUID

from app.services.jump import JumpService
from app.schemas.jump import Jump, JumpCreate
from app.config.influxdb import client, bucket, org

router = APIRouter(
    prefix="/jumps",
    tags=["Jump"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=List[Jump])
async def get_jumps_by_user(user_id: UUID):
    db_jumps = JumpService(bucket, client).get_jumps_by_user(user_id)
    if db_jumps is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_jumps


@router.post("", response_model=JumpCreate)
async def create_jump(user_id: UUID, csv_file: UploadFile = File(...)):
    db_jump = JumpService(bucket, client).create_jump(user_id, csv_file)
    if not db_jump:
        return HTTPException(status_code=500)
    return db_jump


@router.delete("/{jump_id}")
async def delete_jump(jump_id: UUID):
    db_jump = JumpService(bucket, client).get_jump(jump_id)
    if db_jump is None:
        raise HTTPException(status_code=404, detail="Jump not found")
    try:
        JumpService(bucket, client).delete_jump(jump_id)
    except (Exception ,):
        raise HTTPException(status_code=304)
    return {"message": "Jump deleted successfully"}
